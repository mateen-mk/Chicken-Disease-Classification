from ChickenDiseaseClassifier.constants import *
from ChickenDiseaseClassifier.utils.common import read_yaml, create_directories
from ChickenDiseaseClassifier.entity.config_entity import (DataIngestionConfig, 
                                                           PrepareBaseModelConfig)



class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        """
        Initialize the ConfigurationManager.

        This constructor reads the configuration and parameters from YAML files
        and creates the necessary directories for artifacts.

        Args:
            config_filepath (str, optional): Path to the configuration file.
                Defaults to CONFIG_FILE_PATH.
            params_filepath (str, optional): Path to the parameters file.
                Defaults to PARAMS_FILE_PATH.

        Returns:
            None
        """
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])



    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Get the configuration for data ingestion.

        This method reads the data ingestion configuration from the main config,
        creates the necessary directories, and returns a DataIngestionConfig object.

        Returns:
            DataIngestionConfig: An object containing the configuration for data ingestion,
            including root directory, source URL, local data file path, and unzip directory.
        """
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config



    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        """
        Get the configuration for preparing the base model.
        
        This method reads the base model preparation configuration from the main config,
        creates the necessary directories, and returns a PrepareBaseModelConfig object.
        
        Returns:
        PrepareBaseModelConfig: An object containing the configuration for preparing the base model,
            including root directory, base model path, updated base model path, image size, learning rate,
            include top flag, weights, and classes.
        """

        config = self.config.prepare_base_model

        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )

        return prepare_base_model_config
