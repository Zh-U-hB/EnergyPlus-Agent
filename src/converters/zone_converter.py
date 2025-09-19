from eppy.modeleditor import IDF
from src.converters.base_converter import BaseConverter
from src.validator.data_model import ZoneSchema

class ZoneConverter(BaseConverter):
    """
    负责将标准化的区域数据转换为EnergyPlus IDF对象。
    """
    # 构造方法，初始化ZoneConverter实例
    def __init__(self, idf: IDF):
        # 调用父类BaseConverter的构造方法
        super().__init__(idf)
        # 初始化存储转换后区域数据的列表
        self.converted_zones = []

    # 实现父类的抽象方法convert，负责区域数据的转换逻辑
    def convert(self, zones_data: list, remove_existing: bool = False) -> None:
        """
        转换区域数据并将其添加到IDF模型中。

        Args:
            zones_data (list): 包含区域数据字典的列表。
            remove_existing (bool): 是否在添加新区域前移除IDF中所有现有的ZONE对象。
                                    **警告：此操作不可逆，且仅删除ZONE对象本身。**
        """
        # --- [改进] 在每次转换开始时清空状态 ---
        self.converted_zones = []
        self.logger.info("Starting conversion of zone data...")
        
        # 遍历每个区域数据
        for zone_data in zones_data:
            # 验证区域数据有效性
            if not self.validate(zone_data):
                self.logger.warning(f"Skipping invalid zone data: {zone_data}")
                continue
            
            # 转换区域数据为EnergyPlus所需格式，使用get提供默认值
            converted_zone = {
                "Name": zone_data["name"],
                "Floor_Area": zone_data.get("floor_area"), 
                "Volume": zone_data.get("volume"),       
                "Multiplier": zone_data.get("multiplier", 1),
                "Ceiling_Height": zone_data.get("ceiling_height"), 
                "Zone_List_Name": zone_data.get("zonelist_name")
            }
            
            self.converted_zones.append(converted_zone)
            self.logger.info(f"Validated and prepared zone: {converted_zone['Name']}")
        
        self.logger.info(f"Successfully prepared {len(self.converted_zones)} zones for IDF.")
        # 转换完成后调用add_to_idf方法将数据添加到IDF文件
        self.add_to_idf(self.converted_zones)

    # 实现父类的抽象方法add_to_idf，负责将转换后的数据添加到IDF文件
    def add_to_idf(self, remove_existing: bool) -> None:
        """
        将准备好的区域数据写入IDF模型。
        """
        self.logger.info("Adding zone data to IDF...")
        
        # --- [修正] 用参数替换 input() ---
        if remove_existing:
            self._remove_existing_zones()
        
        # 为每个转换后的区域创建IDF对象
        for zone_props in self.converted_zones:
            self.logger.info(f"Adding zone to IDF: {zone_props['Name']}")

            # 直接在ZONE对象上设置几何属性
            self.idf.newidfobject(
                "ZONE",
                **zone_props  # 使用字典解包来设置属性
            )
            
            if zone_props["Zone_List_Name"]:
                # cSpell:ignore zonelist
                self._create_or_update_zonelist(zone_props["Zone_List_Name"], zone_props["Name"])
                
        self.logger.info(f"Successfully added/updated {len(self.converted_zones)} zones in IDF.")

    # 实现父类的抽象方法validate，负责验证输入数据的有效性
    def validate(self, data) -> bool:
        try:
            ZoneSchema.model_validate(data)
            return True
        except Exception as e:
            self.logger.error(f"Validation failed for data '{data.get('name', 'N/A')}': {str(e)}")
            return False

    # 辅助方法：移除IDF中已有的区域数据
    def _remove_existing_zones(self) -> None:
        """
        移除IDF中的所有ZONE对象。
        """
        self.logger.warning("Removing all existing ZONE objects from the IDF model.")
        # 遍历
        zones_to_remove = list(self.idf.idfobjects["ZONE"])
        for zone in zones_to_remove:
            self.idf.removeidfobject(zone)
        self.logger.info(f"Removed {len(zones_to_remove)} ZONE objects.")

    # 辅助方法：创建或更新ZoneList
    def _create_or_update_zonelist(self, zonelist_name: str, zone_name: str) -> None:
        """
        创建新的ZONELIST或将区域添加到现有的ZONELIST中。
        """
        # --- [修正] 正确操作ZONELIST对象 ---
        try:
            # 尝试获取已存在的ZONELIST
            zonelist = self.idf.getobject("ZONELIST", zonelist_name)
        except IndexError:
            # 不存在则创建新的
            self.logger.info(f"Creating new ZONELIST: {zonelist_name}")
            zonelist = self.idf.newidfobject("ZONELIST", Name=zonelist_name)

        # 查找所有已存在的区域名
        existing_zone_names = [zonelist[f'Zone_{i}_Name'] for i in range(1, zonelist.num_extensible_fields + 1) if zonelist[f'Zone_{i}_Name']]

        if zone_name in existing_zone_names:
            self.logger.debug(f"Zone '{zone_name}' already in ZONELIST '{zonelist_name}'.")
            return
            
        # 扩展ZONELIST并添加新的区域名
        zonelist.new_extensible_group()
        new_field_index = zonelist.num_extensible_fields
        zonelist[f'Zone_{new_field_index}_Name'] = zone_name
        self.logger.debug(f"Added zone '{zone_name}' to ZONELIST '{zonelist_name}'.")
        
