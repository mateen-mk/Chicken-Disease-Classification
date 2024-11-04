# Chicken-Disease-Classification


## Workflows

1. Update config.yaml
2. Update secrets.yaml [Optional]
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline 
8. Update the main.py
9. Update the dvc.yaml


### workflow
--- 
- update config.yaml and params.yaml
- create research/notebook stage  # for testing below steps
- update src/entity/config_entity.py
- update src/config/configuration.py
- create src/components/(current stage)
- create src/pipeline/(current stage)
- update main.py



### DVC DAG
---
```dvc
+----------------+            +--------------------+
| data_ingestion |            | prepare_base_model |
+----------------+*****       +--------------------+
         *             *****             *
         *                  ******       *
         *                        ***    *
         **                        +----------+
           **                      | training |
             ***                   +----------+
                ***             ***
                   **         **
                     **     **
                  +------------+
                  | evaluation |
                  +------------+
        
```