import os
from ChickenDiseaseClassifier.constants import *
from ChickenDiseaseClassifier.utils.common import read_yaml, create_directories
from ChickenDiseaseClassifier.entity.config_entity import (DataIngestionConfig, 
                                                           PrepareBaseModelConfig,
                                                           PrepareCallbacksConfig,
                                                           TrainingConfig,
                                                           EvaluationConfig)



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
        --------
        config_filepath (str, optional): Path to the configuration file.
            Defaults to CONFIG_FILE_PATH.
        params_filepath (str, optional): Path to the parameters file.
            Defaults to PARAMS_FILE_PATH.

        Returns:
        --------
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
        --------
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
        --------
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



    def get_prepare_callback_config(self) -> PrepareCallbacksConfig:
        """
        Prepare the configuration for callbacks used during model training.

        This method reads the callback configuration from the main config,
        creates the necessary directories for the checkpoint and TensorBoard logs,
        and returns a PrepareCallbacksConfig object.

        Returns:
        --------
        PrepareCallbacksConfig : PrepareCallbacksConfig
            An object containing the configuration for callbacks,
            including root directory, TensorBoard root log directory,
            and checkpoint model file path.
        """
        config = self.config.prepare_callbacks
        model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
        create_directories([
            Path(model_ckpt_dir),
            Path(config.tensorboard_root_log_dir)
        ])

        prepare_callback_config = PrepareCallbacksConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath)
        )

        return prepare_callback_config



    def get_training_config(self) -> TrainingConfig:
        """
        Prepare the configuration for model training.

        This function reads the training configuration from the main config,
        prepares the training data path, creates the necessary directory for the root directory,
        and returns a TrainingConfig object.

        Returns:
        --------
        TrainingConfig : TrainingConfig
            An object containing the configuration for model training,
            including root directory, trained model path, updated base model path,
            training data path, epochs, batch size, augmentation flag, and image size.
        """
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "Chicken-fecal-images")
        create_directories([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            updated_base_model_path=Path(prepare_base_model.updated_base_model_path),
            training_data=Path(training_data),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )

        return training_config
    


    def get_validation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model=Path("artifacts/training/model.keras"),
            training_data=Path("artifacts/data_ingestion/Chicken-fecal-images"),
            all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
        return eval_config

