# File Structure

- rpi_counter_fastapi/
    - requirements.txt
    - readme2.md
    - safety_instructions.md
    - start_main_app.sh
    - .lgd-nfy0
    - readme.md
    - start_camera_services.sh
    - hailort.log
    - structurefiles.md
    - pytest.ini
    - .env
    - .gitignore
    - .env.example
    - pyproject.toml
    - main.py
    - data/
        - box_counter.db
    - docs/
        - manuals/
            - operator_manual.md
            - ai_features.md
            - ai_labelling.md
    - app/
        - __init__.py
        - websocket/
            - __init__.py
            - connection_manager.py
            - router.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - connection_manager.cpython-311.pyc
                - router.cpython-311.pyc
        - api/
            - v1/
                - __init__.py
                - operators.py
                - reports.py
                - system.py
                - camera.py
                - profiles.py
                - products.py
                - outputs.py
                - debug.py
                - detection.py
                - run_history.py
                - orchestration.py
                - auth/
                    - __init__.py
                    - security.py
                    - dependencies.py
                    - jwt_handler.py
                    - __pycache__/
                        - __init__.cpython-311.pyc
                        - dependencies.cpython-311.pyc
                - __pycache__/
                    - debug.cpython-311.pyc
                    - run_history.cpython-311.pyc
                    - __init__.cpython-311.pyc
                    - detection.cpython-311.pyc
                    - reports.cpython-311.pyc
                    - operators.cpython-311.pyc
                    - system.cpython-311.pyc
                    - camera.cpython-311.pyc
                    - profiles.cpython-311.pyc
                    - products.cpython-311.pyc
                    - outputs.cpython-311.pyc
                    - orchestration.cpython-311.pyc
        - auth/
        - middleware/
            - metrics_middleware.py
            - __pycache__/
                - metrics_middleware.cpython-311.pyc
        - core/
            - __init__.py
            - modbus_poller.py
            - camera_manager.py
            - modbus_controller.py
            - system_orchestrator.py
            - sensor_events.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - camera_manager.cpython-311.pyc
                - modbus_controller.cpython-311.pyc
                - modbus_poller.cpython-311.pyc
                - sensor_events.cpython-311.pyc
        - utils/
            - __init__.py
        - __pycache__/
            - __init__.cpython-311.pyc
        - web/
            - __init__.py
            - router.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - router.cpython-311.pyc
        - services/
            - __init__.py
            - detection_service.py
            - notification_service.py
            - system_service.py
            - orchestration_service.py
            - __pycache__/
                - __init__.cpython-311.pyc
                - system_service.cpython-311.pyc
                - detection_service.cpython-311.pyc
                - orchestration_service.cpython-311.pyc
                - notification_service.cpython-311.pyc
        - models/
            - __init__.py
            - product.py
            - run_log.py
            - event_log.py
            - profiles.py
            - system_status.py
            - detection.py
            - detection_event.py
            - configuration.py
            - database.py
            - operator.py
            - __pycache__/
                - product.cpython-311.pyc
                - operator.cpython-311.pyc
                - database.cpython-311.pyc
                - __init__.cpython-311.pyc
                - detection.cpython-311.pyc
                - detection_event.cpython-311.pyc
                - run_log.cpython-311.pyc
                - configuration.cpython-311.pyc
                - profiles.cpython-311.pyc
                - event_log.cpython-311.pyc
                - system_status.cpython-311.pyc
        - schemas/
            - operators.py
            - run_log.py
            - reports.py
            - profiles.py
            - products.py
            - detection_event.py
            - __pycache__/
                - detection_event.cpython-311.pyc
                - reports.cpython-311.pyc
                - run_log.cpython-311.pyc
                - operators.cpython-311.pyc
                - profiles.cpython-311.pyc
                - products.cpython-311.pyc
    - __pycache__/
        - main.cpython-311.pyc
    - scripts/
        - load_test.py
        - setup_database.sh
        - system_test.py
        - backup.sh
        - install.sh
        - create_service.sh
        - setup_pi5.sh
        - benchmark.py
        - install_dependencies.sh
    - web/
        - static/
            - css/
                - dashboard_v3.css
                - dashboard.css
            - js/
                - operators.js
                - reports.js
                - dashboard.js
                - status.js
                - hardware.js
                - run_history.js
                - gallery_usb.js
                - dashboard_v3.js
                - gallery.js
                - products.js
                - connections.js
                - profiles.js
                - gallery_rpi.js
            - captures/
                - rpi/
                    - event_7354a6e1-f306-457d-b8ec-bd76958618d1_1755090487.jpg
                    - event_d614c2bc-0857-4d41-aca1-b544c4473d17_1755082779.jpg
                    - event_be52b08b-9aff-494a-b8e6-98fb8615bf7b_1755086135.jpg
                    - event_f503771b-0ad7-403c-9c62-c4af8de56b49_1755088112.jpg
                    - event_94a8ca0b-585b-4fd1-8990-7b1c5c38b226_1755092144.jpg
                    - event_1f6fd52b-6562-4e6c-a482-9dce6680f138_1755087258.jpg
                    - event_a77ab7f6-d70f-4910-919e-d58762c8a772_1755085070.jpg
                    - event_c3bd3ee6-ec35-4ad0-a759-67ec42f179c3_1755092264.jpg
                    - event_64f193be-6ca2-489d-bb93-dfed13cb243e_1755087219.jpg
                    - event_6a795e50-0ecc-464b-a4c2-8319737e8d6d_1755086054.jpg
                    - event_3748af02-01fa-4078-9340-ec4e27df8b27_1755083271.jpg
                    - event_62b1e830-db97-4649-a1b2-f57c93f87c4d_1755083304.jpg
                    - event_021b7631-7a26-4b26-ad80-5109bf3ed133_1755084924.jpg
                    - event_636d4b6d-2433-472b-b530-a6232851aa2f_1755087565.jpg
                    - event_e8e0e77d-cdfd-429e-b650-d57a829a551d_1755084949.jpg
                    - event_1a30b890-e03a-4d57-8629-28082efa9fa2_1755082624.jpg
                    - event_48e35680-023e-40b2-8493-880f5661828d_1755087414.jpg
                    - event_26384db9-6df3-4c2c-a11c-0ad7c4d4c293_1755090097.jpg
                    - event_bff92b37-d020-471a-8a4e-8befe9a4f330_1755092134.jpg
                    - event_f080755a-e6ae-492b-a84f-c8f021d2157b_1755088345.jpg
                    - event_66d368ff-9925-456c-809d-d9f89eabdafe_1755082705.jpg
                    - event_735981bc-a9f7-4099-8b89-dc6e37679248_1755090452.jpg
                    - event_084dfaca-b7dd-44e9-8cf6-0b5e3b56f389_1755084470.jpg
                    - event_c664d651-258a-46d6-a1c3-9dc88f77c047_1755091559.jpg
                    - event_0a78d1e3-3a98-4b7c-8b27-169719874271_1755091403.jpg
                    - event_9381d506-f697-452d-b7c9-3d0be635d529_1755088065.jpg
                    - event_94863f6d-2e55-4a0f-be64-b27df1a05ded_1755085642.jpg
                    - event_201ad3c1-e167-43fc-ae25-fbff3981b9d6_1755087473.jpg
                    - event_882d818d-56b3-44c2-b485-b7837fcfe8b8_1755085473.jpg
                    - event_424747d4-7fae-4a1d-8248-3f3600101e51_1755092079.jpg
                    - event_fd520c1a-ea55-4e1e-8602-9d70e5078305_1755088833.jpg
                    - event_5f60b74e-6a66-49f3-a225-ec500c9e2259_1755084439.jpg
                    - event_1544828f-ca43-481d-8f77-71159969ee3c_1755086431.jpg
                    - event_87457990-8031-4b3e-80a7-2e599f7394cd_1755092000.jpg
                    - event_7ea6112f-8a98-46a1-8e60-0f5602a806f4_1755083875.jpg
                    - event_ca94732d-a85c-4201-be19-f3d7662b12d1_1755086369.jpg
                    - event_abe4e103-c394-4dd8-9d08-7f16377d8ef6_1755091343.jpg
                    - event_5c92867b-eacf-4ecf-8d6a-5be695c7dd02_1755082627.jpg
                    - event_40a14ca8-819e-4c57-a1ab-047196bfea92_1755090987.jpg
                    - event_05c86cd1-102c-453e-ba5a-69bd2babef63_1755087534.jpg
                    - event_43927db8-0cc1-4549-98f8-9c31d243d8b2_1755086941.jpg
                    - event_0842bc06-6c22-4044-a914-93e1c7ea8c06_1755087067.jpg
                    - event_60ba0cdd-1738-4f52-80c7-3597065f0d94_1755085143.jpg
                    - event_3fcf3d5d-524e-4be8-94a1-5ab70604e541_1755083478.jpg
                    - event_a2ff1ab1-258b-4cf8-87cd-4ab13885b6fc_1755087037.jpg
                    - event_92a40ca5-9e43-4e75-b2fa-89b339aa01a8_1755082563.jpg
                    - event_1dec8f46-a2cb-4893-98dd-acc2c52d9b26_1755084775.jpg
                    - event_ae0b5293-208b-47fb-8f24-d5c4636212a2_1755085616.jpg
                    - event_072d3fe6-cf5f-44e9-9db8-be51253f48c1_1755090000.jpg
                    - event_165791a3-8076-406e-a5aa-7f223734e379_1755091943.jpg
                    - event_a3d64312-3643-4720-9104-4d5a1b25cfec_1755086357.jpg
                    - event_06348092-e822-49c5-9061-ad2dc827bcb0_1755082882.jpg
                    - event_395778aa-319a-4f0d-b04a-16c076834969_1755082818.jpg
                    - event_c528152c-1cf1-4d01-9023-fbc58274df67_1755087437.jpg
                    - event_9b582513-20df-47f6-b00b-75649bd3e86d_1755091024.jpg
                    - event_ccb4a75f-9c8c-460f-af1d-72ce0d5ac960_1755091536.jpg
                    - event_b124a010-0154-4196-91a0-eaedc688e3b2_1755082643.jpg
                    - event_78f86f84-0846-4528-a299-54dd1fd92a0c_1755090079.jpg
                    - event_c080c71f-31f2-4f58-a263-1d32484d3c83_1755088095.jpg
                    - event_bf7fbf1b-9699-4b79-9278-c71ca6953ca2_1755084646.jpg
                    - event_23d822f5-b19e-4841-8e45-9a366351a6fb_1755083288.jpg
                    - event_0f9de4db-1ff9-447b-afc4-2c8ff10389d4_1755087211.jpg
                    - event_ea7a8190-08e1-4799-8988-3e4a91f03da8_1755087511.jpg
                    - event_c0aa01b2-7913-4416-a14e-e42977f0636d_1755085990.jpg
                    - event_0c6bbdb1-98ef-478c-9a85-591d59eaff4c_1755089908.jpg
                    - event_a3252601-ea85-4ad5-a1ab-0ed84f4f3d0b_1755091882.jpg
                    - event_25eee38c-0fc6-4f60-b8cc-c791d728f5d0_1755084996.jpg
                    - event_44284f3c-8bf4-4770-b6b4-1ee481878717_1755089625.jpg
                    - event_47675c3a-c78a-4c15-b625-e7b4f862c438_1755083250.jpg
                    - event_0dfcf61c-c2ef-465e-afae-84f3e54cfc6f_1755090336.jpg
                    - event_1905a77b-857f-4e69-9687-00aee36dea53_1755089192.jpg
                    - event_32b3f419-90a7-46df-84f4-2bcfee81af45_1755088073.jpg
                    - event_58095ad4-c222-4b1c-b0b3-9f1402d88f2d_1755082552.jpg
                    - event_482842b7-22f2-4081-9e04-17b69c375792_1755083459.jpg
                    - event_10f79a16-72b8-44c5-b006-cb73782f0b2b_1755088309.jpg
                    - event_7eb48ba3-14f4-4e09-9c52-485656edc048_1755091261.jpg
                    - event_ae1c385f-3664-4646-a028-2c14cd92d7cf_1755087178.jpg
                    - event_86d27d6c-8105-48a1-add0-6de0847f87a0_1755089318.jpg
                    - event_a9afdb07-2f55-490d-adaa-a593ad750879_1755085996.jpg
                    - event_cdacea87-dff0-4aef-8cee-174058350440_1755084622.jpg
                    - event_4574286d-1823-47fa-a565-2f2a57ee4764_1755088049.jpg
                    - event_e4b2e65f-4414-422d-801f-0a600065b24b_1755088140.jpg
                    - event_f9069a74-f446-4769-8d3d-5c8acaa42691_1755084305.jpg
                    - event_9c491476-0165-4fc1-84ae-37214071f464_1755086575.jpg
                    - event_f20ea464-0d37-4722-981f-eec799b5da31_1755088182.jpg
                    - event_c448eaf7-d849-46e6-8020-a4e50b7fd7a2_1755085672.jpg
                    - event_60d3ba69-114d-49b9-bdaa-48c1455211be_1755084400.jpg
                    - event_70ce050a-8d41-4a1a-a2da-15c4a5ff4d90_1755083826.jpg
                    - event_87a4140a-75f1-4c4f-a672-99f14d4b1ba7_1755091152.jpg
                    - event_1a16dacb-92a0-46c0-be13-ad52426c1960_1755090301.jpg
                    - event_8fd40d97-a426-4a61-8b64-a49542ed5db8_1755091059.jpg
                    - event_e49d5767-24c2-4d83-a102-9d461791d7e5_1755084430.jpg
                    - event_3354964c-78df-4a5c-ab41-df8b7fd7e342_1755091467.jpg
                    - event_a6a09ab0-bdd2-43db-8da9-f1ffea3e24cf_1755092018.jpg
                    - event_5a620180-ba81-4960-ae45-0a6cc3b7cf8a_1755091991.jpg
                    - event_13091cce-0c9a-4204-9b2e-8a6c5c43602c_1755084927.jpg
                    - event_c8f74240-6d0b-4f12-9603-4b52ff2a32ae_1755087597.jpg
                    - event_333681d8-c9c3-4680-9b0d-b05e05e30e8c_1755090991.jpg
                    - event_57d03c50-98c0-4277-ae4f-3de1bb8eb850_1755084760.jpg
                    - event_407e688c-41a1-4ce6-895f-0d9d1eec8c29_1755084063.jpg
                    - event_07db9a6d-8e1f-4924-8a28-a12b53d95339_1755088167.jpg
                    - event_b5e5affb-e15a-48da-bb8c-b02f35dda22b_1755086954.jpg
                    - event_87008148-9221-40a9-b5f5-9eff1abab2fd_1755082596.jpg
                    - event_c030175f-4333-4d32-a4de-874e41ab50c6_1755085713.jpg
                    - event_a6881dc1-380f-4d7f-8e97-2bdb54c8dc6e_1755088201.jpg
                    - event_859ab63c-22ef-4730-aab3-bace3c7c03cb_1755084079.jpg
                    - event_038c8055-8f4e-44ad-bd19-963067e58db3_1755089860.jpg
                    - event_9c41ed26-f853-4a0d-8789-4eb2abccbc12_1755084379.jpg
                    - event_69146278-d796-4c5c-b748-39c8e865c645_1755084795.jpg
                    - event_4d5db5ae-9d53-42e7-a5a6-0aca10a3a8a3_1755084495.jpg
                    - event_4907287d-5529-4554-afb9-5389ab474851_1755084555.jpg
                    - event_4b99f26e-4546-4f86-b4f3-167607e7a700_1755085094.jpg
                    - event_857850d3-46e7-4c28-913b-795a4a21fb4f_1755087267.jpg
                    - event_bba3d72a-ac38-40b9-a0e0-948a90fa6d5b_1755086468.jpg
                    - event_155acedf-b1cf-4164-a726-1d4b64d5a4d5_1755085976.jpg
                    - event_0365fd6a-a256-4968-a21c-97b024d7590b_1755090518.jpg
                    - event_c021adc0-91db-4ec1-8444-8cce868e4596_1755084418.jpg
                    - event_0ea9bc3c-678b-4c04-99ac-8f0f207781ee_1755086105.jpg
                    - event_d01aebb5-3aa4-47e2-b3b4-8515ffdae5c0_1755083319.jpg
                    - event_919704bd-88aa-402d-a978-eeda4a41dad2_1755090945.jpg
                    - event_6f788bc7-7f47-404b-83da-4b3dc4249115_1755090492.jpg
                    - event_6fc92a54-17fe-40f1-b3bc-e4e5e682c19b_1755085466.jpg
                    - event_f8cc8745-6069-4df8-8801-dabeb7bd6e07_1755090456.jpg
                    - event_5646109c-5bb5-4b98-86ea-f70a5e9f9061_1755085703.jpg
                    - event_c88cd780-74b3-4f24-84ae-17573173d358_1755085482.jpg
                    - event_dc8eae71-35f0-4f3a-bd24-c208e4e0cf29_1755089877.jpg
                    - event_998dc398-d028-4a2e-a8e2-8814690e2efe_1755085074.jpg
                    - event_188a9670-9458-4f59-a23b-ce8a332142ee_1755089242.jpg
                    - event_d2882cc8-fbcd-466a-aad5-33ea664d949f_1755088327.jpg
                    - event_c46a7af2-40c6-4782-b935-7bb85ea4582a_1755090430.jpg
                    - event_852e1e5b-a052-47ef-a05d-46eb6b00dc8a_1755086310.jpg
                    - event_cda56783-bab6-41c3-8f2e-39ff1716ffef_1755088246.jpg
                    - event_68f2babd-912a-4b79-9e5d-1d36cd3fb658_1755090245.jpg
                    - event_45eeac47-e700-43ea-a2bf-498cc196bda9_1755086710.jpg
                    - event_50cfa19c-b7ac-446c-8fd5-90f5455e10d1_1755085547.jpg
                    - event_9d4f355e-8459-4355-b418-b8936580bbac_1755087143.jpg
                    - event_d5bd8995-2368-43eb-93a4-2dcae0594ee8_1755086629.jpg
                    - event_b7ad0c64-5c4a-49a7-9717-c97108dd2e90_1755092178.jpg
                    - event_fb62d318-7e7e-455c-b711-ac1293751bad_1755089110.jpg
                    - event_d2b427ce-cf8b-420a-8e10-abfd292981d1_1755085659.jpg
                    - event_117f7687-0d0c-4280-a98a-85c34b8f05e8_1755083409.jpg
                    - event_0676a9bb-c312-438b-923e-6a49ea37a6aa_1755087847.jpg
                    - event_d1eaefde-35f8-42b9-bb2e-dbedea8372a3_1755085985.jpg
                    - event_52f37d55-8615-4963-8cb4-8fe57b4004c0_1755090331.jpg
                    - event_da244f46-80d7-4049-92be-618686a46b24_1755091103.jpg
                    - event_2afae6e3-e91a-4d76-8f1f-1f9d64dd2bd7_1755087490.jpg
                    - event_060552b9-987c-49ad-904b-27d60aa79195_1755087651.jpg
                    - event_445fa9ed-4ee4-48bc-a842-218e5017f6cb_1755088231.jpg
                    - event_d6c07710-0784-4732-a8ba-1a8780b17289_1755088283.jpg
                    - event_675db5d3-aa9d-4d88-83c7-7ede7c904aae_1755092104.jpg
                    - event_84bf69fb-1cd8-4393-a82b-0471009617f6_1755086699.jpg
                    - event_78a68fba-97b8-40e0-a33e-9ea04ee6bb52_1755085060.jpg
                    - event_fdcf1dcb-0750-48b3-978b-7a93008066db_1755086385.jpg
                    - event_80f401f3-020c-42b5-a97f-2df5629c6421_1755092052.jpg
                    - event_e9adbec5-4b26-4e80-ae31-0de39ac31c0a_1755084914.jpg
                    - event_e9cba896-2a63-4703-a7a5-0fa9c8dfcca0_1755087999.jpg
                    - event_27795a41-c833-4bc0-a574-7bc0cfcb8c83_1755085109.jpg
                    - event_b3e05c31-2213-47c6-9b4b-95fd95401d33_1755084352.jpg
                    - event_9a2271b7-816e-4483-9f6e-913d0be0cc68_1755087107.jpg
                    - event_48dbcc72-58e7-41b3-a2fc-75cfdf5baaf8_1755090159.jpg
                    - event_a8d2b711-b3e1-45a0-9965-a7e4cd8e738a_1755084457.jpg
                    - event_de215892-4df9-48e4-92a4-676a78e41d81_1755084295.jpg
                    - event_13bd7b06-7f0b-4159-97be-242256762f95_1755084907.jpg
                    - event_f23f1834-cbd0-4977-88a5-2b00a2bf8545_1755091420.jpg
                    - event_2e390e16-3ad3-4b8e-89ec-a7b0e0fafe92_1755082513.jpg
                    - event_4e125bfe-c60b-4dbd-ba54-238b082cb2b4_1755088080.jpg
                    - event_3c0c6339-38fe-4b06-8458-9f65874c93dd_1755091010.jpg
                    - event_96ea5ed0-3ef1-43ce-8d60-ab0afde77b0c_1755090576.jpg
                    - event_014c11ee-6ebb-4285-88d2-f52012bafa4a_1755083428.jpg
                    - event_5fb37791-9358-4600-8eb9-c3843404b36a_1755086961.jpg
                    - event_cb42c7e0-4cc9-42d7-aa37-607505921a55_1755084968.jpg
                    - event_f32aa41c-606b-480f-b4ad-8a82727e2657_1755084632.jpg
                    - event_1ed204ce-4c35-48d6-b187-634bc41a6069_1755082517.jpg
                    - event_d384cb28-71f0-45d1-b7dd-249ade6b457f_1755090189.jpg
                    - event_54a0401b-71a4-4350-bc2d-d3a6e62f7a4e_1755087911.jpg
                    - event_a79ce3ec-9c49-433e-ba3f-3298720ee5c8_1755083833.jpg
                    - event_08ef519e-a3b8-43cc-891c-2e11fdfc36f5_1755087164.jpg
                    - event_0ec080fd-b41d-49a8-8fcd-7e1304abf177_1755085669.jpg
                    - event_18743225-5908-4ce8-b0ea-7c6567685057_1755082711.jpg
                    - event_a3006b59-44c9-4367-8836-1829bc190a1c_1755086163.jpg
                    - event_bf6abaf5-990c-4118-b0ba-3ce7c1f76322_1755086179.jpg
                    - event_c658f6a3-5e2e-46ce-84ff-e60cbca9e539_1755090064.jpg
                    - event_c9bf4ca9-4316-428d-b749-c53b54dd829c_1755087643.jpg
                    - event_e91c8ecc-ad69-417c-9396-80e28b4b0378_1755086905.jpg
                    - event_ebc00e74-ecac-4e75-b3cf-f901f2b52454_1755086026.jpg
                    - event_c765ace3-af30-4d94-bba0-22063d44954d_1755087750.jpg
                    - event_a5a1bd70-61fd-4005-a3ae-9fee3fa5acef_1755092127.jpg
                    - event_c332d94b-3109-41ae-9f3a-0c56c11dd1df_1755091208.jpg
                    - event_9d97e9af-2c11-4f7b-93b7-295c87d4b3a9_1755084993.jpg
                    - event_144a1c12-2c07-4a41-b1e3-e8919acabec3_1755089222.jpg
                    - event_74593e2b-9ace-44c2-bae1-3d3a60b027a3_1755091779.jpg
                    - event_ba058e63-5b0f-446e-9412-cd1f1b8de3ed_1755086634.jpg
                    - event_f2cf47c0-16ce-4190-a9d5-d9312ef14c94_1755085682.jpg
                    - event_0be18f8b-cd96-4f19-b804-8bbe2643c19c_1755085603.jpg
                    - event_e92d4dc8-8172-47d0-8d34-ec14ca709dc3_1755087898.jpg
                    - event_587f285a-9a92-43fc-a96e-78bed0c98480_1755085623.jpg
                    - event_b4401625-6aab-44c6-9e40-ce47d9c8f9ca_1755091439.jpg
                    - event_52cbc707-11d5-4786-85cc-370fd12f7c08_1755088160.jpg
                    - event_7f7e6ecc-7409-4351-b574-09fa12f24809_1755087043.jpg
                    - event_28b6d2c8-28da-4799-8869-0b0b01827cdb_1755091826.jpg
                    - event_70c44743-bf16-435c-be05-9ad4c06453c8_1755090314.jpg
                    - event_8b99c793-4637-4feb-8d46-592e5ae0b9ce_1755084028.jpg
                    - event_394acd17-498b-4df2-af5a-a1aa4e7365c9_1755086171.jpg
                    - event_eae0014f-0280-483b-8f0d-9c2db0ccbc60_1755082857.jpg
                    - event_44cb217b-ca7e-456b-a650-f45293bb991c_1755085958.jpg
                    - event_24a177e0-166c-48db-a04e-c2bbaa1c0483_1755090358.jpg
                    - event_81288044-2bf8-4625-a32f-3101b69d22f2_1755090320.jpg
                    - event_c66f90a3-f472-4f9a-8376-7629332d7dbf_1755089132.jpg
                    - event_34da3773-74a5-48f1-94e2-4b61b2d59ee9_1755085573.jpg
                    - event_93ee6880-f3e2-4ddf-834f-485fb41d3521_1755085126.jpg
                    - event_644b966e-147e-4d54-9c29-5db8d0c3b30b_1755091362.jpg
                    - event_d3b819b1-8f21-49d4-8101-0ce7f883c163_1755091805.jpg
                    - event_69a1a54e-f72d-45a4-8e22-9301307dc4ef_1755082523.jpg
                    - event_3a05d8e2-b493-4766-991d-fc286db3f5b7_1755086421.jpg
                    - event_f8cb980b-876a-4731-b5ee-9138b27d1a21_1755085953.jpg
                    - event_23100b6c-8923-4c9e-9092-49f1d1408096_1755089036.jpg
                    - event_21a7bcf8-5d5f-4184-8d94-ca4e86532cde_1755091088.jpg
                    - event_3b5b44e6-7038-4471-a3a8-5d9309cce453_1755086696.jpg
                    - event_9392f650-d7a8-4a85-995e-6f7717163298_1755085066.jpg
                    - event_1a45dd06-7e3c-43d9-98ba-b7b0422d8efd_1755085539.jpg
                    - event_da6428a6-73c0-4c9c-b33e-577e0ea9956d_1755085981.jpg
                    - event_9842f05b-c649-4123-9c8e-33d019740bb2_1755084838.jpg
                    - event_1e97386c-1029-411f-94c9-9f3976686f0c_1755085008.jpg
                    - event_01e4a610-556f-4e9f-8d12-5bc09f334345_1755088222.jpg
                    - event_2e04cd2c-6150-429f-829e-83f4358b384e_1755084843.jpg
                    - event_bbf2ff94-46a5-4b5d-ae5c-66cafeecc319_1755084263.jpg
                    - event_7a3a8b94-81e5-446a-97f2-fadaff88d3da_1755091244.jpg
                    - event_b4a814c2-12fe-4b7f-8f9c-aff019964cfb_1755092229.jpg
                    - event_3bbe7a38-e1ce-4ce0-8cfd-3c519598ae04_1755083964.jpg
                    - event_ef82a40f-1960-4f08-9ecd-74521a6bafdc_1755088837.jpg
                    - event_25a1623b-c94f-4d8c-a4f5-a910fb256db8_1755087982.jpg
                    - event_c8dc7b3e-35ec-4af4-adf7-b4fc042ad2cf_1755084314.jpg
                    - event_5e647b50-fde8-49f9-90b0-6a156ea795b0_1755087326.jpg
                    - event_e0148063-3ed7-47f5-baf7-e18cfa4818c8_1755085536.jpg
                    - event_ff9ee454-b7ef-4426-a454-79c1922971eb_1755089201.jpg
                    - event_331ace0d-8a92-4161-b8bb-79cf16cc14a8_1755091147.jpg
                    - event_c1c390a3-afb0-44f7-b6e5-4d3c503f1952_1755084389.jpg
                    - event_2077f052-5872-43e4-bae0-f4e68256513a_1755090281.jpg
                    - event_e188946b-65ca-4fb9-865d-b50bcbe17675_1755083936.jpg
                    - event_b9e4953c-9327-4088-b5d3-f5984bf6f409_1755082892.jpg
                    - event_ce46750e-d5a6-46a8-9d4d-b11c2336bc61_1755087206.jpg
                    - event_6d464c45-9eb3-4fb0-b2c0-ce045a309aae_1755084802.jpg
                    - event_4124c0e3-b3cf-4b67-9a5e-6b17e4b94d62_1755088286.jpg
                    - event_339b3f7a-eda6-4bcb-ac16-e6ab02367b3d_1755089065.jpg
                    - event_a8d5a391-8836-4830-9543-973c1fa1554d_1755092203.jpg
                    - event_83054b16-3edb-403d-a9c0-446d4ddd9091_1755084169.jpg
                    - event_80f10acb-0752-44c7-af1a-5df5ccef3750_1755086396.jpg
                    - event_0f34715a-3c59-449a-902a-33f9c751f7c0_1755085700.jpg
                    - event_0749d9d7-6b02-4864-9d1c-699920e81f10_1755087825.jpg
                    - event_4ad75ddb-601f-47a9-9621-652e22a047fd_1755084807.jpg
                    - event_b18a1a06-475f-4ab1-9f3b-919e8c0d49c6_1755084635.jpg
                    - event_39a96a50-c40e-4ab4-80b4-0214734d9ea4_1755090144.jpg
                    - event_29c2da12-6286-4f06-a72f-1e377e0e0b8b_1755091450.jpg
                    - event_31cb8662-7ebd-43ca-bb88-1c39a4b4e97b_1755085964.jpg
                    - event_b1bc15c1-0111-452b-9d59-ec8fada58ae3_1755087124.jpg
                    - event_4483251a-82fd-453c-b9c5-3b7279d7a315_1755087055.jpg
                    - event_ea831747-69c2-49ce-b0d8-65f79bb9b7a5_1755084798.jpg
                    - event_2da061f6-7544-4d37-9e13-2219fe06f709_1755087346.jpg
                    - event_19935fef-dc0f-4644-8d34-dfd41fc4bc5f_1755088809.jpg
                    - event_9a138974-238b-47af-809b-759bcea71cf3_1755091851.jpg
                    - event_fbb8408e-c44f-4983-a7d0-461e95ece304_1755087226.jpg
                    - event_2afef0f8-56aa-4cce-a940-4d492671b28a_1755085663.jpg
                    - event_9e0663bf-aa30-4f96-9fe4-3edd0d44c016_1755086639.jpg
                    - event_42390868-a9a0-4625-8669-875212a035de_1755085638.jpg
                    - event_9bdc8133-43ae-4648-895c-7f5173855f05_1755084583.jpg
                    - event_dd79965a-6c7a-43bf-a85c-6d6ec37470e2_1755085707.jpg
                    - event_42fc6a52-a680-40af-9c44-6fe8d74c026c_1755088043.jpg
                    - event_1bd1b989-73bb-48cf-ab16-e1df0101e0a0_1755085462.jpg
                    - event_e651cbca-9b74-4c80-8ddd-3b850e577155_1755085527.jpg
                    - event_0d873faf-ded5-4398-bc03-0cef1d34e203_1755084921.jpg
                    - event_73bfc1c1-db47-4086-9b78-bca63cb4ba15_1755086391.jpg
                    - event_2d899a30-d661-48d6-a364-3075e03a52e2_1755084986.jpg
                    - event_dbc3985d-a17d-46c2-b6f0-4dc7e7e22c85_1755082493.jpg
                    - event_6ee3c75c-c245-4176-9335-3a80758c4655_1755084523.jpg
                    - event_fc07a37a-2e55-4188-994f-3901882fd6c4_1755085183.jpg
                    - event_da9a15ff-7718-4968-a564-ad1f23b16934_1755082590.jpg
                    - event_470e7122-8d86-48c9-a795-0b9e5d7d727d_1755085971.jpg
                    - event_066bc7e7-353b-4dca-ac49-98752fa73b6c_1755089251.jpg
                    - event_deb4b235-7a2c-443f-961a-5e5554c96475_1755087186.jpg
                    - event_24734e95-5121-4ab6-8443-005a876090f6_1755091756.jpg
                    - event_a2ff2b7c-b6c3-435f-a91e-4ab354b8b363_1755087393.jpg
                    - event_1d1af3b4-dbc0-4f3d-b1c7-de2b1f4fa174_1755090797.jpg
                    - event_c87dd026-56df-41c9-8852-09abd07e3f94_1755084360.jpg
                    - event_7bc2d876-b6d6-4b0d-8ec6-b67c62569b5f_1755085653.jpg
                    - event_4fa8257f-748c-4ac4-919c-82864412711c_1755090404.jpg
                    - event_fa6155f8-b47c-4d0e-bd9e-1e0fb1c693b5_1755091603.jpg
                    - event_a22c114a-7fc5-4407-a19f-95fc8c42d8aa_1755086155.jpg
                    - event_f2daecbf-bb9a-411a-9ee4-d29f6acba1e5_1755082736.jpg
                    - event_e048041e-0409-42ba-9beb-f8fa4061ab81_1755086003.jpg
                    - event_64084cc2-d4c8-401d-923d-c606ca18fe33_1755085091.jpg
                    - event_1e57d149-c114-418f-bf7a-b363bc3e2aea_1755085504.jpg
                    - event_8f45733e-4124-45aa-af78-a647429ebbfb_1755091049.jpg
                    - event_23e8f3bb-3ec7-420e-8fed-56da0e50cf9a_1755090041.jpg
                    - event_79fd8b71-018d-4990-8d3f-d4734cfa7eb5_1755084766.jpg
                    - event_62dfaa8d-9e85-4193-b495-dfa3021855c2_1755091511.jpg
                    - event_303e68aa-311f-47a2-8008-a6547785fb40_1755087312.jpg
                    - event_8eba2cc2-de04-4b31-915d-71770d035cf1_1755089284.jpg
                    - event_36b66140-cf27-48e9-a8d2-924ab3124a19_1755084593.jpg
                    - event_9bfcb01b-c66c-4808-888b-ffaa5af223a1_1755087604.jpg
                    - event_febd29e3-0119-4bc9-b5e7-0e29b60a0327_1755084998.jpg
                    - event_db8648e4-367d-4f30-9b31-6ecf6573bebb_1755085137.jpg
                    - event_61ef6a46-f314-4b1f-9f38-ad1e86db7e83_1755087090.jpg
                    - event_0f091c40-42d5-422a-ba77-b30543576a62_1755091884.jpg
                    - event_8b7e1af3-2cd6-453b-aaca-0b0af360b404_1755091005.jpg
                    - event_da4dbfe2-d53d-43ae-8c4c-6f6b6921ac33_1755085684.jpg
                    - event_9ef4d2ed-34aa-4c57-b29f-b5f382b735a3_1755091072.jpg
                    - event_60abcca9-1573-465a-85fa-c4602581214c_1755086010.jpg
                    - event_2b318759-06ce-470e-b31e-2e02415e9b08_1755084509.jpg
                    - event_01d92c0f-9432-46c5-93ea-48d6cad939d8_1755089230.jpg
                    - event_7111a91b-ad43-4a5e-9852-d0de50d630d2_1755090239.jpg
                    - event_4eee1600-0e1e-40c7-9849-e13fe1e19292_1755090412.jpg
                    - event_051ed5c4-2cbd-4c16-8a70-70d846334d71_1755086131.jpg
                    - event_fcf3a37a-76d8-4d3e-b4d3-64e60c14c72b_1755087975.jpg
                    - event_61001ec4-3947-4537-8889-9742dd02ec1e_1755089271.jpg
                    - event_368d1110-4e08-436b-9dc7-f757b15019ac_1755084096.jpg
                    - event_54eb1a66-3dd1-48e5-be2f-4398fed60611_1755084852.jpg
                    - event_05513203-7103-4a50-aa14-b99e1aeda87e_1755088087.jpg
                    - event_adbabc0e-3bd7-457f-b227-ab4f44cd5181_1755083388.jpg
                    - event_fad357d2-8563-4679-8bf4-e897bb669f8f_1755089879.jpg
                    - event_9ef12204-93bb-4e4c-9d7f-37249315aa0c_1755084769.jpg
                    - event_af328579-d081-49f9-a956-791e69d50686_1755087092.jpg
                    - event_b0a00254-d3ee-414d-ad19-3002bd03ab6e_1755091951.jpg
                    - event_c408799b-71fd-42dc-84a3-4a20f75165a7_1755084129.jpg
                    - event_e705fa92-8ca6-4b7b-958a-30ef23d9fe02_1755084825.jpg
                    - event_24fad088-d1dc-4f54-bf7f-d6741d75ec12_1755086884.jpg
                    - event_c2ded620-1a88-4731-a2d5-d967011f3396_1755087112.jpg
                    - event_26175d68-54dd-4966-af4c-ea97125a0ffc_1755085522.jpg
                    - event_f02c8eb1-05a9-4982-a31d-a30f5e520fba_1755091982.jpg
                    - event_2e6720dc-73c5-47f0-a7c1-3d14c106e8b9_1755085657.jpg
                    - event_5d7881c9-491d-4a70-a06e-12960508ee6a_1755091251.jpg
                    - event_f4582b79-c74e-4b78-ae88-a63d220127a3_1755083262.jpg
                    - event_3c4aab03-da07-44a2-881a-5ec8f2088a7a_1755091503.jpg
                    - event_8399ce90-89bb-451e-9b05-a414c7c3f72a_1755084989.jpg
                    - event_e237b9a0-9252-4643-b23b-882f34f7494a_1755090166.jpg
                    - event_e2f04197-6299-43b9-b6cc-02ca52d635e7_1755090408.jpg
                    - event_eeedc8e3-2a77-425e-bf94-0c38ee918350_1755086401.jpg
                    - event_6acd41fa-20e4-406e-a650-3dd53fdce38a_1755087853.jpg
                    - event_5d845757-13a5-4fb3-9bdd-0e2b0b563398_1755086936.jpg
                    - event_e38903a2-e60b-4267-b999-dd341f56d892_1755086414.jpg
                    - event_077c5b22-2952-4e74-b9e3-d3227a781f6f_1755084935.jpg
                    - event_922e372e-b812-473e-87d5-6da026ffd73a_1755084917.jpg
                    - event_83842ed8-4de7-4dde-b1db-cf8358e138ac_1755091158.jpg
                    - event_557a3866-a56e-49aa-9ab8-d19fcb45bb47_1755087692.jpg
                    - event_f96a2d43-13f3-46f7-8481-7e641d9e367f_1755085688.jpg
                    - event_3004d2d0-f9ba-44a4-bc82-ae4bb310a794_1755086087.jpg
                    - event_41687188-d538-488a-a96b-2d28ba834c5b_1755087007.jpg
                    - event_a3d50b16-bcee-4d9e-bb8f-ba2435748689_1755084651.jpg
                    - event_723631d8-f7d1-4660-b082-096158416797_1755082573.jpg
                    - event_305f73c9-469a-4b22-a5c4-6656420d2bed_1755083995.jpg
                    - event_1c4db0ee-a6b5-49fe-99a9-ef107da3274e_1755090113.jpg
                    - event_746823a9-2e59-43d8-b6f7-3fde74ce9fba_1755085611.jpg
                    - event_e42b9546-f657-4b6f-83d1-8bd2b34ac69f_1755088216.jpg
                    - event_25064a2d-d848-4620-a02a-24ac5e4f3c43_1755091682.jpg
                    - event_b5e90571-f32b-4f1c-a225-943b39516c6f_1755088821.jpg
                    - event_47b322bf-431d-4731-a373-faab70ea8151_1755083488.jpg
                    - event_e0c1fd5c-561f-4c09-8535-c34d59f85989_1755086058.jpg
                    - event_a60634af-4e2e-4d05-9da1-ab63ee950a8e_1755087192.jpg
                    - event_3c1c37fd-6141-44b4-a416-c7cd1a28ac01_1755086410.jpg
                    - event_09625bf7-b4a1-4c39-a2e5-fc8cbd510da8_1755085103.jpg
                    - event_6fcdd9de-2031-4118-a48e-e012df107415_1755084338.jpg
                    - event_bd0df87a-ef04-4b90-b2e9-539ae51721a3_1755090072.jpg
                    - event_787c6028-c184-43a9-8402-bc7980bd0371_1755091002.jpg
                    - event_a95a7fe2-1de1-4015-81b8-79058f3be9a2_1755091387.jpg
                    - event_cf5b40c0-c817-49c5-8f4a-9f6a3c37a961_1755090465.jpg
                    - event_9ae24264-7f00-4fe9-86d3-5d1d5a1247d9_1755085531.jpg
                    - event_caa75354-c261-45ba-967f-3eb1d4d2751c_1755084531.jpg
                    - event_84138e5e-f261-4db6-bfdc-87b298c3c420_1755084772.jpg
                    - event_dcc26a20-f2f9-4331-ad17-817f31e79315_1755084884.jpg
                    - event_b96fa7dc-d17c-4592-9b2f-7ca58c4add05_1755087797.jpg
                    - event_82bcf141-f560-43b7-b625-1d8d43020a98_1755082667.jpg
                    - event_60a4b0d5-72a1-4f8b-b5b7-fb7847068402_1755086911.jpg
                    - event_d5297878-8eec-457f-bf4d-e086078c195b_1755087285.jpg
                    - event_8cc32b07-321b-45cb-9070-6fd327c1d1e4_1755082682.jpg
                    - event_3cfb8298-75bc-4580-8239-21b401c91b69_1755082620.jpg
                    - event_45e9b07d-7cb4-490e-85b4-3ac764761d0f_1755084859.jpg
                    - event_fc2b61c9-376f-4eb3-9749-9063331bd4c4_1755090259.jpg
                    - event_f57d172b-926c-4146-a277-2fdc25e02b93_1755083328.jpg
                    - event_16673e2a-874f-4701-b043-cac0cbbcc8a5_1755086068.jpg
                    - event_0e0a6f75-8d5b-4d74-bac7-f418d2c1fce7_1755090296.jpg
                    - event_82107ea8-bc01-4566-8e3e-a4ad8ba2fa2f_1755085146.jpg
                    - event_b1ea93ef-0062-47aa-b0ba-f4e69e7d2cd0_1755082867.jpg
                    - event_2acaf411-e74d-465d-83bf-76a96580e2a2_1755085881.jpg
                    - event_487c6840-4750-4b32-9365-aa03d1fb65ab_1755085877.jpg
                    - event_8c30fc00-87fd-4591-8f29-57a09e5d41ea_1755087966.jpg
                    - event_0bf61c96-2f43-4489-ada2-ebf5523a5a69_1755086100.jpg
                    - event_55b0c258-edf8-4fc1-8e47-dc5194812b11_1755082767.jpg
                    - event_b16f670c-8968-40ed-afaa-2678d6dbdb05_1755085140.jpg
                    - event_a7e6b99b-d7c3-4922-975d-64f9e60b9b39_1755084945.jpg
                    - event_e30b5e21-7963-4099-896d-35f1c2e616ec_1755086947.jpg
                    - event_114dadb1-3925-4187-9308-c09acd7f382a_1755084658.jpg
                    - event_06e8af2b-9705-4fca-a187-2bac9a28189d_1755088009.jpg
                    - event_8465a2cd-ad2e-48c9-8581-a1212cfcd516_1755089600.jpg
                    - event_1901908a-e795-4ae1-8948-5d7527a83460_1755085133.jpg
                    - event_aec89a0f-4016-4a25-b737-864941453a22_1755086612.jpg
                    - event_046790da-1103-436a-9800-f4fd213fde8b_1755083846.jpg
                    - event_5e0a77ff-7e46-4736-9e13-0e466b806e45_1755087588.jpg
                    - event_76102313-883e-4bad-a6da-a194e25c35b9_1755088928.jpg
                    - event_2b5a8f52-61f5-4de2-ab45-341997e583a1_1755082608.jpg
                    - event_9ccabe22-af12-4286-accb-af354dffb9e3_1755087484.jpg
                    - event_9c475a5d-1297-46e5-9c7e-1df76f605b88_1755087030.jpg
                    - event_00cdc747-c476-480f-ba49-37f0727d5ac2_1755087817.jpg
                    - event_e3dde003-5f17-46f3-b87c-308c1f7877e3_1755088850.jpg
                    - event_cb8a7523-5b2c-4884-b097-185220e94e63_1755089120.jpg
                    - event_d20b7fbd-e552-4315-a1d7-6dc085888494_1755084833.jpg
                    - event_418e828c-d5d3-4626-8f63-83510b6f7064_1755091192.jpg
                    - event_fdcd26a5-7ce3-4c2e-a202-d56189ca5123_1755087536.jpg
                    - event_a51c7291-20c0-427d-bb73-4edbca878fb7_1755087577.jpg
                    - event_96aa8642-9e1b-435a-9f5a-b80af3cbd1d3_1755084325.jpg
                    - event_d9ae0d33-70c1-4abd-ac46-1d19a7ec9022_1755091716.jpg
                    - event_9003275d-ddba-4600-9667-2ff89c112a41_1755087943.jpg
                    - event_7d15876a-8c82-4e67-aadd-c08ec81214d7_1755086675.jpg
                    - event_f3b825f8-2ec1-4368-86b8-d4c37c1c018a_1755091118.jpg
                    - event_5b8b2e4e-212d-4200-8028-f0ca5210fc0a_1755082727.jpg
                    - event_030ce587-d3a4-4be8-bfe4-11ba00f9064b_1755091658.jpg
                    - event_19126d2a-1540-4f24-8e31-f08ed2eecfcd_1755084675.jpg
                    - event_af7a19f0-c485-4dab-b53c-64ca885bb8ff_1755086583.jpg
                    - event_7c699ace-9135-4a2d-9cba-b8ff6c36480a_1755083888.jpg
                    - event_3f7f7143-e91e-42e2-9f77-57253f56467b_1755083419.jpg
                    - event_10381bd5-fdf7-4a7c-9831-b22de42fa0d9_1755084626.jpg
                    - event_c17f31a2-690e-4e6b-91ab-0089874f58b7_1755084612.jpg
                    - event_770f8649-7e96-4cb9-bca5-8e57ac2f8a49_1755085099.jpg
                    - event_dae7a490-8874-45d4-ae2e-c61ac5a28a5d_1755084978.jpg
                    - event_54fc2790-801c-43c9-b6fe-8e00f4c52fd0_1755087629.jpg
                    - event_fdbafcd3-029d-45ca-b384-b266019a681e_1755090422.jpg
                    - event_cae7abfa-6969-44d0-97db-137779fb9612_1755085696.jpg
                    - event_28f78686-c512-4d8d-887c-bcceb159c906_1755090051.jpg
                    - event_f8cd5106-0034-44b3-962e-ee9edd9cc8d4_1755092220.jpg
                    - event_093ccc1f-562d-4fca-bda4-d51ebb82cdd1_1755091182.jpg
                    - event_bf22ac7a-034b-49c3-bb71-5b9fa8b0a956_1755085490.jpg
                    - event_ce1807b9-d831-41e9-af86-2cb40217a69e_1755087149.jpg
                    - event_3973310d-c644-49c7-8bf9-610db54fd86f_1755091084.jpg
                    - event_02f5fedc-4a90-4c95-93c2-489856c56ab2_1755084370.jpg
                    - event_844ad053-a29c-4a00-95a2-371616a70410_1755087711.jpg
                    - event_5384cc31-7183-4699-9790-c1ad5a8e3439_1755086350.jpg
                    - event_6e413042-d830-4455-a4ed-65f48d0d2865_1755086643.jpg
                    - event_f4e3a369-4be0-4cd5-be56-4957f63baade_1755090952.jpg
                    - event_3cf92529-5578-4e83-8cc1-4e8be03602a3_1755089868.jpg
                    - event_64614198-750b-4498-a09f-1d7c9dc24ad7_1755092166.jpg
                    - event_3f56ada1-9eef-495a-8dea-b2daa3c894f3_1755090978.jpg
                    - event_c09ce78b-2d92-4e20-a926-7d98c9597a08_1755084111.jpg
                    - event_118b742a-5a20-4475-a43d-d673595080fd_1755087305.jpg
                    - event_80d1af4f-6e26-4f31-83aa-482effd70562_1755085910.jpg
                    - event_94f481ce-e16c-4712-ac27-0c35fc0200a1_1755086678.jpg
                    - event_d89da7ca-be69-4327-903e-1cb0dbf74c1d_1755087467.jpg
                    - event_fbee1bca-de10-4f81-95d1-bceebafeb5eb_1755082688.jpg
                    - event_97b672ff-b070-4345-b83e-2424b26b7290_1755087904.jpg
                    - event_2887d8bc-60d1-4b90-adcf-01626a70b44c_1755090544.jpg
                    - event_21ad187d-58ec-4407-b1d1-57fb699612ea_1755090013.jpg
                    - event_689d05df-b1e0-41e3-acdf-a231cad903f1_1755087926.jpg
                    - event_2e79e8cf-7f6b-41fa-bb1f-68a17fd6cf21_1755088261.jpg
                    - event_7e0f708d-7c19-4d75-8d86-a1ce0672fc0c_1755086047.jpg
                    - event_7951d994-1520-47c3-8124-9a2802563272_1755090369.jpg
                    - event_3ae709d5-3396-4a12-a6af-03288b7b9fe8_1755085082.jpg
                    - event_ff31f2b2-669c-4daf-baa3-46e560b3f3c7_1755087319.jpg
                    - event_14a5250c-2f72-412c-b9fa-454de69093e6_1755090566.jpg
                    - event_c6c0b526-80da-4336-8d91-c70303a23888_1755086705.jpg
                    - event_d7b243fd-0e20-46bd-98c6-89e3e9df3422_1755085690.jpg
                    - event_5ea8adfb-f907-4840-b8d1-107faac08d64_1755085676.jpg
                    - event_7e8c48db-cd70-465a-9548-1a48b46650a5_1755091578.jpg
                    - event_e3a019e2-706b-4e14-985e-3b8f373e037a_1755085057.jpg
                    - event_8031f7c6-5374-439e-9d77-e07f2ec371ab_1755087431.jpg
                    - event_2d4a8074-963b-4040-947b-dfc3408d486c_1755089980.jpg
                    - event_93be6bf0-82f6-4b28-95db-19545a6faa9f_1755089157.jpg
                    - event_142d56ab-a5ba-4cb2-b2e9-e2f58312ed15_1755090552.jpg
                    - event_ae20bb4b-d517-4856-aaa6-b3c470e07290_1755082871.jpg
                    - event_730e63bd-8b7e-4e6b-881d-16fb656726f7_1755083400.jpg
                    - event_50065da1-399e-4126-96f8-ef7c7676ca90_1755085078.jpg
                    - event_10ac67dc-fad9-4277-8e79-6b9b003cfe02_1755085628.jpg
                    - event_576a6fd2-9a11-41c1-807c-fe9be35f5db3_1755086990.jpg
                    - event_f54bcf54-17ec-4566-a400-5ebfc49e7697_1755086475.jpg
                    - event_cf94adf8-cc30-43c4-a73c-b4345def5a64_1755087610.jpg
                    - event_dd2f4f45-f195-4749-9b73-7e3f1f401ddb_1755087017.jpg
                    - event_3bab131b-5ef7-422b-bc4e-6b6eb7cdc426_1755087543.jpg
                    - event_c2a003c2-262e-4ca1-a80d-ce978d849318_1755085890.jpg
                    - event_9c264ba7-4cbe-44b1-b9a7-a4ae8a6b6a19_1755089960.jpg
                    - event_ab3f6866-1b92-4f6a-a16e-dfec4429f617_1755085717.jpg
                    - event_b15d4e21-bf6b-42a8-95f5-f0938952357c_1755084482.jpg
                    - event_950b1ca7-815e-4b55-8e3d-3a5c668f35a6_1755089618.jpg
                    - event_9259036c-a0db-4b38-98eb-62ca7d920605_1755086608.jpg
                    - event_db27e6c1-bd72-4c45-afbe-8f1dbbb29c98_1755086077.jpg
                    - event_98fdbb68-fcfe-4fa2-857f-c69aa19a8a53_1755091622.jpg
                    - event_33848291-305d-49ac-849a-d258f008f5e3_1755090470.jpg
                    - event_ddb3bc89-4e56-42f6-b9e9-484d0da9e472_1755091045.jpg
                    - event_1a3745da-368d-4803-a492-2e757030179e_1755090476.jpg
                    - event_c40b916d-c425-4dcd-a48d-fa1e1e5a54dd_1755086194.jpg
                    - event_d80eeb84-9617-4acf-8771-f9490fa96b35_1755086204.jpg
                    - event_3f63e5e3-5bb8-48d9-bfb5-5c30052ab584_1755088298.jpg
                    - event_e78b5ce7-a279-4c95-95c9-0513441c5b77_1755084956.jpg
                    - event_dd764503-4aca-4d4e-a7ef-554c0ad7c9e4_1755087503.jpg
                    - event_fbb679bd-45c9-4520-b6f7-c85300e7d02c_1755090223.jpg
                    - event_9f0e4695-1405-4a6d-bd0f-a752009193b1_1755090364.jpg
                    - event_d458617e-a088-403d-9ec3-f13ac284c067_1755082538.jpg
                    - event_9505985a-ef63-4b29-ac81-1b9cf6b3f38e_1755087073.jpg
                    - event_c64da6e9-7efc-41d6-b2a8-c6aa3606d9aa_1755084971.jpg
                    - event_51654bcd-4143-47af-a21b-69eefad3267d_1755084603.jpg
                    - event_a6cc7bf8-cced-4073-81ce-11b2c6471e83_1755089138.jpg
                    - event_df3283c7-c259-4c1b-87e2-ffd7d10b71e5_1755091921.jpg
                    - event_1a3946e9-fb68-4071-a5f8-13d2adfabf98_1755089901.jpg
                    - event_ee6be651-7c78-402f-9337-825f4a16665c_1755084785.jpg
                    - event_82cd72e5-4c7e-451e-aa33-1851dd4adea8_1755092062.jpg
                    - event_e845e0b9-8d8f-47a8-9484-48d6dbedff58_1755085947.jpg
                    - event_ee7cf5bc-5a71-4e3a-bcd7-7b7e3673ab0e_1755090572.jpg
                    - event_6aa7ed0c-ef16-4e1f-9db2-89c4ad53e6b5_1755089310.jpg
                    - event_4ae168e6-9036-4039-9ce2-212808d39406_1755087496.jpg
                    - event_532aa672-e5b9-4246-bd9c-8b876288a031_1755082618.jpg
                    - event_c6883533-d135-4d1c-b98d-aba503be84d2_1755086200.jpg
                    - event_66496cc8-83f9-403d-abc3-cbe7097b30fa_1755087841.jpg
                    - event_3fefb05d-102f-4715-b424-bad7c9d06caa_1755091210.jpg
                    - event_ac9208a9-97a4-4465-8656-90b2914ba72c_1755090058.jpg
                    - event_41811f41-a5e7-412d-95a2-7333d0dbac1b_1755086061.jpg
                    - event_f812d2ba-13d4-433f-a9a0-59cda00a1f96_1755085902.jpg
                    - event_65e4b0f6-b677-4f5f-9a3b-4cd5dbf5a3a0_1755082697.jpg
                    - event_77631fcf-04c0-4531-852a-2ad41854078b_1755087636.jpg
                    - event_56a0a18a-2388-418a-916e-9566f422bba1_1755088121.jpg
                    - event_faa2f3ac-2e5e-4a93-a545-80d95c40a25d_1755089915.jpg
                    - event_9477eb89-dd46-49f3-83c4-674481aeffb9_1755091833.jpg
                    - event_5d9f5dfc-93a3-4174-a0fd-0cb8e61c88c8_1755082886.jpg
                    - event_517183a6-d4ce-4f5f-8724-af8e58b51d48_1755090174.jpg
                    - event_a2db91f0-e881-494d-956e-0c9e0a37ba77_1755084847.jpg
                    - event_9d481d60-f47b-4a3a-babb-e695f418ec5e_1755086570.jpg
                    - event_55b1e2df-a23b-4771-8f80-09f9b17c4b36_1755091394.jpg
                    - event_45e451f8-93f7-48b7-bcc2-da97d25aa780_1755082812.jpg
                    - event_b2905af7-8768-4590-a1a3-0a4ac108c3d7_1755089279.jpg
                    - event_324af2c4-3579-4640-9bd0-9115d2121586_1755091265.jpg
                    - event_72476f53-a0b0-4c35-914b-313aa08fe0bb_1755090788.jpg
                    - event_6c790955-97a9-42b6-b609-87567d30f3b5_1755092253.jpg
                    - event_70294e58-f9ee-4fb4-b957-0e0beb9d2ccd_1755086125.jpg
                    - event_f373cec9-5442-497d-9173-7eb8096e04c7_1755087341.jpg
                    - event_4762835c-8a0f-4575-ae7c-5ef7febb218f_1755091909.jpg
                    - event_8ce91dba-51e4-413b-8253-6e3f9a58215a_1755082840.jpg
                    - event_74242f63-e73c-44f6-b767-eb63faf8e969_1755090401.jpg
                    - event_b3eb8107-0400-466d-a1e0-6c3cebb56c7b_1755088238.jpg
                    - event_1de6129d-5c6f-479d-bdc8-2ac10f20d606_1755085485.jpg
                    - event_f0becb1c-df07-4e86-bc29-9c6311500010_1755085508.jpg
                    - event_b084aea1-97d7-4856-8f96-fbb3ceabe0d1_1755084490.jpg
                    - event_532af917-1c98-4faa-9b67-4120db7357fe_1755082496.jpg
                    - event_68682158-5ed7-42fe-b6d0-3f958b7b2c69_1755085479.jpg
                    - event_f14f6785-b647-407c-87fa-7679398a22a8_1755091179.jpg
                    - event_1f526c44-7ad9-4f0d-9c29-365ced129969_1755087726.jpg
                    - event_ad21bad6-98de-41f1-be23-5ba3f3a25069_1755082633.jpg
                    - event_7e1a48da-8a49-445e-9040-9a34c8f97113_1755092031.jpg
                    - event_1c69d00f-1162-460b-8aec-fe9dbe25101b_1755084959.jpg
                    - event_a84c6412-c3e1-4302-b9d7-46cfaa8c29db_1755089328.jpg
                    - event_c6b42467-1ddf-4051-8669-b2771607a4cb_1755088101.jpg
                    - event_f59d48de-9a8f-4382-8907-e99e8c9d751b_1755090390.jpg
                    - event_13f74151-0ba7-4fe3-b607-da59f04b52ec_1755082833.jpg
                    - event_7cc83d77-7f39-43be-993e-e53ccfd7fa4a_1755087660.jpg
                    - event_1dc595b4-721f-4ee8-9433-011a60d26b41_1755087449.jpg
                    - event_d19aced3-fc0b-4a30-8163-510ec883256b_1755092194.jpg
                    - event_36a3e8a6-35a4-4916-9cf1-20fb619ae2e6_1755089262.jpg
                    - event_899e0f76-64c8-4d58-97b0-84b16f691bde_1755087370.jpg
                    - event_cb25b9d8-749e-4c05-9b61-9083164d9ca3_1755086930.jpg
                    - event_f7c412b3-5ed4-4066-bacf-7cbc484bafbf_1755090087.jpg
                    - event_df6b0cfb-d692-4796-80b6-4ce682300cb8_1755091624.jpg
                    - event_4ee16eb2-b96b-4121-ab2c-c03e420e20c7_1755086149.jpg
                    - event_15e3f541-5da8-4046-9ae5-5b872838093e_1755086119.jpg
                    - event_29b02340-a593-4732-91e4-deb709997179_1755092112.jpg
                    - event_7b13e5aa-94bb-421a-8ffc-ab2b0a0a8861_1755087951.jpg
                    - event_cf75e3c0-8b0f-4bc0-8440-a2fe13c26acb_1755083910.jpg
                    - event_95aac480-7635-4e14-9fb8-bfc5fbdd3a21_1755083280.jpg
                    - event_15b4fa5c-b902-45f5-a0b6-387b754c2a01_1755091547.jpg
                    - event_45ea0767-4bdf-40fc-95b2-3507d395da1f_1755087273.jpg
                    - event_cf80dfb3-a54f-4be7-9446-639961505baa_1755091873.jpg
                    - event_cff37c4d-9532-438d-8310-ecb979345aa5_1755091704.jpg
                    - event_f13f291b-6c35-40bc-8986-613bb013f536_1755087099.jpg
                    - event_aaaccb91-7603-4a1a-af9b-0955aca4b2b5_1755087666.jpg
                    - event_cce97334-9447-487a-aa58-6128089b23b2_1755082905.jpg
                    - event_5ec1bf56-e0ac-4f06-ab9c-272645a5e5e9_1755082534.jpg
                    - event_b2f7b203-ca26-4bbc-9ee9-24d74682ea97_1755086219.jpg
                    - event_4b6b4e36-413b-4d11-b719-be7f4e59611f_1755090437.jpg
                    - event_c331723c-ce3c-4bb7-a5b8-856d6bbbef6a_1755092088.jpg
                    - event_fd6f0ea7-0538-4a60-94df-1b1a6190bc66_1755087553.jpg
                    - event_88c66e38-e77d-41a4-8e61-25dfeeca859b_1755084273.jpg
                    - event_1c3d0eee-63f6-46d4-a05f-11f56d02d938_1755091187.jpg
                    - event_a795ecf5-06b5-4dbf-b1a1-4a01e132ec42_1755085456.jpg
                    - event_878328bc-9d56-47a7-9e07-a77b765c879e_1755084952.jpg
                    - event_af33c9c3-740d-4784-baf3-fc30c2937ef3_1755087615.jpg
                    - event_f5f59873-2277-408f-ba2e-090c137162ac_1755084285.jpg
                    - event_54b82591-ea6e-4cf3-ae2f-9c5c69d8a68d_1755086878.jpg
                    - event_ff76d968-379a-4736-a9a2-c9d037ad4b2c_1755085459.jpg
                    - event_0d911b7d-8813-4756-bec3-940ba51b8d16_1755087918.jpg
                    - event_c2d7f39d-9725-48f7-9cf9-81b2108ae875_1755084975.jpg
                    - event_851d41ed-c4d8-49a3-b66d-26558e1c3fa7_1755090549.jpg
                    - event_e92ae227-6654-46c1-a490-af1a81658986_1755086601.jpg
                    - event_f13360d8-4463-44de-bdee-d4e143230d65_1755088844.jpg
                    - event_49e9b407-18c0-41c7-9432-18f856ae75b3_1755089968.jpg
                    - event_4baca90e-b956-4912-980a-170982542c7f_1755084599.jpg
                    - event_96730470-69e8-4c33-a3f1-7d28ae065d12_1755091611.jpg
                    - event_3c935e76-bd73-495d-b591-8df3b448bf40_1755088252.jpg
                    - event_0b19c192-fb80-430a-b14c-9f6801054ec9_1755089053.jpg
                    - event_e369a273-bd84-437c-a6b3-df0e566d831a_1755089947.jpg
                    - event_8af4c224-cd4c-4328-bb7d-b2b8c2124763_1755087131.jpg
                    - event_46632dd2-3e45-48aa-a4ce-58d342f84f14_1755084498.jpg
                    - event_8f3266b1-dbe9-46e4-9cde-1c5ad8181ba5_1755088153.jpg
                    - event_f09abf33-1fcc-4355-b4ca-6020373174eb_1755090956.jpg
                    - event_807af608-95f9-4bf9-8ef9-bbe5d7ef4787_1755087401.jpg
                    - event_ce636d64-a15d-4d5c-8b99-af81af656bf8_1755085498.jpg
                    - event_6a9792f2-54b5-409b-8dc5-507a2ff681ac_1755089931.jpg
                    - event_0dea81ad-c725-45a4-9230-a1543eed893c_1755085444.jpg
                    - event_30dc05f9-0787-4753-92f0-5045f42b8c0f_1755090468.jpg
                    - event_c7b35e32-e49b-4c5a-823d-280389ce2ee1_1755087279.jpg
                    - event_9161d98c-981b-4168-a5a0-080de38bf90b_1755090292.jpg
                    - event_7452666d-1d7f-434d-94eb-e9eb6e23da3c_1755086142.jpg
                    - event_fa72e4f4-9154-4a71-8d3b-b1afdd95e308_1755089836.jpg
                    - event_b395e5b6-81c7-4507-8658-f3f7d1975fba_1755085515.jpg
                    - event_0ef75a18-55a6-4252-bc8f-51329311a539_1755085543.jpg
                    - event_023c31eb-7f2d-4662-8234-6a6c9df5c7a3_1755086417.jpg
                    - event_f5d38ac9-a060-4ba3-bad2-172b5d747717_1755086381.jpg
                    - event_1a69b31e-3feb-43f8-b153-da9e4758f548_1755090809.jpg
                    - event_4726e0df-9b05-46de-a967-9d6d8aa2c2bd_1755090498.jpg
                    - event_fe0170c0-65ae-497d-8457-ea5d8a2c77f4_1755091428.jpg
                    - event_fe436997-60ae-4e7d-a041-060021dfc233_1755091648.jpg
                    - event_313973be-9dae-40c5-8dc2-3e7f801bac7b_1755084445.jpg
                    - event_0cd49ece-6796-415d-aff6-38599585785b_1755086651.jpg
                    - event_73e55098-391c-4430-aade-ffb93fb2c95d_1755085594.jpg
                    - event_5f8c1f84-b4c5-4d1a-b02b-7aa8942eea05_1755090394.jpg
                    - event_c01e36b8-d820-44bb-94d4-69228f40bf72_1755084548.jpg
                    - event_fb493677-c528-43e1-b645-6aa3a146670f_1755085887.jpg
                    - event_f97de340-72d5-4514-9334-9be94c551a27_1755082807.jpg
                    - event_46a86ed1-5372-4704-a3aa-64f1930ce169_1755084016.jpg
                    - event_db70e74e-91da-4440-8393-00238359de18_1755084819.jpg
                    - event_fcebfb66-4489-43ae-8ed4-77377db2bd43_1755090275.jpg
                    - event_b242f9a1-6311-4531-bf46-c02d413c2b4d_1755084562.jpg
                    - event_c9d6af7f-03c8-4269-b416-d0f18f9c1eea_1755084872.jpg
                    - event_3be2df00-e07e-4478-9223-513e0dd1b8bc_1755091223.jpg
                    - event_f249acd6-1d9f-450f-95e4-bc226ecabb26_1755086896.jpg
                    - event_62ff25ee-0552-491b-91d8-259b641b3ca7_1755090231.jpg
                    - event_a36f8ad0-5424-4182-bfd0-d6b491507bcd_1755084829.jpg
                    - event_c2e81c96-93b1-42e9-853d-0d0f450eaa30_1755085029.jpg
                    - event_936f9ae4-8bc7-4e2b-8e63-63e83dfddb4a_1755082547.jpg
                    - event_9232bd7a-cdf4-45a8-9121-62c445dbc694_1755086453.jpg
                    - event_55750bc8-f807-403f-8658-c47162b45c76_1755091013.jpg
                    - event_9539765a-ea61-4207-b2d7-b7f8212088ae_1755084052.jpg
                    - event_6fb33b59-ba82-4563-9ab0-2e233074386c_1755090972.jpg
                    - event_0f3f26b9-6248-42fe-ae65-a0f73f733fb7_1755084408.jpg
                    - event_23be4ed3-2397-4cda-b94f-754dfe5d948f_1755084962.jpg
                    - event_6e8065cf-e281-4940-9b31-d5471837b45b_1755083296.jpg
                    - event_beb646cc-36dc-4fb4-a119-0b6652d775b3_1755091797.jpg
                    - event_a69f664a-4ba0-45cc-a70d-458dcef310ef_1755082639.jpg
                    - event_7e5a208c-08c7-49a8-9a76-99af5b891680_1755087935.jpg
                    - event_e311a499-261e-4a4e-a62f-2bb492f6fd33_1755091863.jpg
                    - event_4f4287bb-95c6-4c1f-9458-b7a8526c5013_1755091098.jpg
                    - event_b7fb981f-8855-4b7b-8341-acd13eb92cde_1755090447.jpg
                    - event_c439d2d8-7d19-4837-bcb2-c45ae2fa7735_1755086436.jpg
                    - event_4909a211-9938-41cd-b987-3782fae3ef04_1755091168.jpg
                    - event_7944f0b1-13c8-47f6-b461-0e57da7757e4_1755086377.jpg
                    - event_4f40c44c-aa15-4ad9-98ab-2e02eb0155d9_1755083437.jpg
                    - event_3b92ff73-31f9-4954-b0b4-380c2c5189f6_1755090949.jpg
                    - event_34fabfb1-bc8a-4f33-9be7-b09400c47cf9_1755084575.jpg
                    - event_68389d51-df4a-4df6-acfe-fe79f02df21c_1755091077.jpg
                    - event_69de36d6-eb0e-4f15-9871-297be4fff244_1755091595.jpg
                    - event_3762c580-25b7-49a4-a164-c1b314516255_1755082772.jpg
                    - event_3be4bc16-4abf-4f25-820d-6b0793b3830a_1755091494.jpg
                    - event_9ffd4211-aa38-463e-82ba-fbc9dac0e374_1755086919.jpg
                    - event_13b398d5-1380-4a61-b652-d0900fdda41d_1755089058.jpg
                    - event_43b92e44-fe0e-4bd4-98a6-492261b53eba_1755082675.jpg
                    - event_8c6dc777-6658-4f76-92d7-36ddbb319c6a_1755089923.jpg
                    - event_233c7106-4cc8-4f0a-a96b-76c18204dc51_1755090522.jpg
                    - event_fe5fe2e6-051e-4067-b911-18ffdf5a8b77_1755086340.jpg
                    - event_a468bb23-ec75-45f7-9298-e56b3d7eb919_1755091215.jpg
                    - event_966cd936-ff97-4ff7-a4a9-ada814266460_1755086604.jpg
                    - event_c7f41018-cf89-49cc-9375-bc09500ba439_1755085519.jpg
                    - event_afd9ecf6-413e-4475-8815-ab2453474755_1755091725.jpg
                    - event_03111ea3-68e9-4451-bf8e-0bcc627fcd04_1755091458.jpg
                    - event_04b4e4c1-5395-42ad-a35f-f419b50cef91_1755082568.jpg
                    - event_a7474c9f-78bd-402f-8e7b-b4f7031b2aec_1755090831.jpg
                    - event_d66b09ac-7d2b-4cd6-8499-8437497df4df_1755091815.jpg
                    - event_e98cf6b3-a6e4-44a0-9559-08ab6194e895_1755086858.jpg
                    - event_00066c9c-dde3-4dc2-afaf-9a0b32dbf2c6_1755092043.jpg
                    - event_e85c655a-5329-4cef-ad11-28ade908f508_1755085053.jpg
                    - event_409ee59f-ff6c-4985-9ae0-6ed829d9d7fe_1755082578.jpg
                    - event_52b96622-93df-4961-9c6b-a2dc04da8220_1755089576.jpg
                    - event_6fa967dd-6b40-4fd6-8778-3122df5b08f6_1755082847.jpg
                    - event_4e140088-7c47-46a3-9547-042d1b3a62db_1755085631.jpg
                    - event_75665022-8910-40c1-a691-473ed4ce0d01_1755088318.jpg
                    - event_f99243c6-1042-41b1-8377-4f1e3d165329_1755086426.jpg
                    - event_2e3d9237-c290-4e18-b929-37d289bec1ce_1755085014.jpg
                    - event_a7a47c27-7f43-4a9f-a21b-d8909f470fa3_1755084911.jpg
                    - event_6d0c2e15-27a3-43be-a308-9b11befcb413_1755085511.jpg
                    - event_e7eb414b-0c6c-440d-9851-6e13fbb2e4a5_1755089388.jpg
                    - event_4ab66bac-38b5-46dc-b3bb-b858c126fc9f_1755085469.jpg
                    - event_67c52466-adae-4e0d-b903-d07fad900458_1755090515.jpg
                    - event_524626d7-d5c3-4b51-9993-174689dc9ae6_1755091173.jpg
                    - event_2841e493-7651-455d-b084-2d78e2d89361_1755086623.jpg
                    - event_4c9fab25-efb4-4562-a080-666f309bad68_1755085898.jpg
                    - event_f91ae184-48b6-43d7-8801-9bc201d247de_1755085492.jpg
                    - event_39b32d95-50c1-4d31-8649-14674545d364_1755086364.jpg
                    - event_4c5efc58-77e1-429b-846f-bbe1d0c197bd_1755088031.jpg
                    - event_3bb5ab08-2d51-43c5-b451-85671a043902_1755085666.jpg
                    - event_e75b8dbc-42cf-4710-a4cb-828e5634842a_1755084486.jpg
                    - event_ea41fe49-ca4d-4ae9-95d7-c6ce56c64100_1755091204.jpg
                    - event_c1c8b635-c253-4ff1-bf09-e2d441bc37cd_1755091644.jpg
                    - event_9c94168a-1b26-474a-a6ba-5e6ffa2c4481_1755082615.jpg
                    - event_f5649628-a889-4d03-a9d0-6f4334af8da9_1755085863.jpg
                    - event_77872d0a-8db8-414f-aa8b-882afaf5db39_1755085939.jpg
                    - event_590b80b3-9381-42a2-8ff3-9983daef193f_1755087157.jpg
                    - event_60c57aeb-4f48-4a23-a498-e7c16c8ac2cd_1755086850.jpg
                    - event_7107a0ab-26a7-4e5b-8a58-fbe63357db2e_1755086669.jpg
                    - event_ae726715-12c7-448c-a312-838f9d131815_1755090254.jpg
                    - event_afa5e1c5-36ad-4f34-ba93-0dc1e98a3a0b_1755084608.jpg
                    - event_90bf3b4f-d5c9-4a9a-84a1-eefa2b9817c2_1755085920.jpg
                    - event_ff2c247c-0024-40dd-84a7-d77d3af0226e_1755091142.jpg
                    - event_95c6ce8b-4859-4f3a-8d41-977dd4c84740_1755091961.jpg
                    - event_bba030f8-22c6-4697-a033-b661552d2bda_1755086647.jpg
                    - event_83b9d1ee-9c42-4d60-babd-a714f4305647_1755090814.jpg
                    - event_10318527-079e-4711-b3b6-55562993bc4d_1755086315.jpg
                    - event_6a9aa0eb-7cd1-463a-87fd-8c48e79a5256_1755086406.jpg
                    - event_94528c2c-a1d7-4bca-bab2-e59178b3ad04_1755085916.jpg
                    - event_6cc89168-c84b-4967-9ce2-789bd3360eb3_1755089817.jpg
                    - event_5d6cd452-cd21-4124-adce-4457fb155631_1755087883.jpg
                    - event_618ee93d-7039-47c0-ad05-ee84a1f81918_1755087119.jpg
                    - event_6995f6c2-663e-4323-aba1-b4d917a0d9ef_1755090963.jpg
                    - event_da993d3c-8b86-4a49-8c30-e7659d0314ee_1755091177.jpg
                    - event_5f0d8490-85bb-4a7b-8875-cb5f53ba8d5a_1755090802.jpg
                    - event_d0701caf-4ffa-4f0a-a8ba-600cdc75949a_1755087421.jpg
                    - event_8a621869-421b-458b-b222-3b0a86d48d48_1755085693.jpg
                    - event_11de9621-20ed-4555-bbc4-b3a72b7b9e78_1755084703.jpg
                    - event_09538632-abb3-4a35-a464-a1dc11df1a37_1755089303.jpg
                    - event_1b10cbdd-9cc7-44c8-a296-c97b0faf51b3_1755086015.jpg
                    - event_4f76dafb-7bc7-4381-bcbb-ab8d55373b2a_1755087518.jpg
                    - event_2b7b84f2-6e4f-4977-9a19-25533d88248e_1755087768.jpg
                    - event_78893c18-ebd9-4de9-80cb-e169ac2b10e7_1755085019.jpg
                    - event_ec0dfb4d-d58a-4a76-ab4b-6621477ac627_1755082543.jpg
                    - event_4c6d782d-9738-4ed3-9ec3-be6a17a8bbba_1755090481.jpg
                    - event_e8ccba40-e03c-48cc-be91-fbe8abf49706_1755091587.jpg
                    - event_9adcb4e8-a85d-4a04-9507-ec6adc51b78d_1755084641.jpg
                    - event_31267368-58fc-45da-8957-e6d64e5fedb5_1755087061.jpg
                    - event_a40f0866-3c1c-4261-8439-dc11437aab72_1755086998.jpg
                    - event_a120a89c-1685-4ddc-a1a7-9211f07c9f6f_1755087378.jpg
                    - event_cd464293-fe15-4c84-8cf5-677bb9649c12_1755083312.jpg
                    - event_89f22912-c414-4754-92fa-d45e4b5a234c_1755090820.jpg
                    - event_3ae21a95-8ff1-46cc-99a8-af21911bf9e8_1755087234.jpg
                    - event_111d92c4-c7ec-4b12-8516-67cd39074bc9_1755086664.jpg
                    - event_60e3441d-1528-4c2e-978d-d28b9bc3fc47_1755084670.jpg
                    - event_9b4a1585-383a-4af0-ab76-1983f361b4b8_1755090310.jpg
                    - event_4cf31040-789c-4888-953c-d4146e018464_1755091230.jpg
                    - event_3480a4ff-22f0-4756-98aa-500cc8348f98_1755086844.jpg
                    - event_87c51344-c5fe-4c98-8a96-54d28873a786_1755091380.jpg
                    - event_a4d2bb7e-9aa4-4f27-bcfc-3a8689903671_1755084983.jpg
                    - event_0374b3a5-fa41-471c-ba06-05a285ed01e5_1755083860.jpg
                    - event_5d3e9891-be9d-4407-b4e8-16d42f8515ae_1755082509.jpg
                    - event_5d1d4c94-4504-4c9e-be7e-c3f710412e77_1755086346.jpg
                    - event_73cd16da-9b8c-41f8-b086-383f3d62e731_1755085501.jpg
                    - event_651e77a5-eb38-4518-80c6-476c4cfe07ad_1755085130.jpg
                    - event_2e2de8f8-e21a-498b-8c01-dbb1d7953b9d_1755087245.jpg
                    - event_ef85794a-a509-40f4-b628-0ed5b836fd10_1755087621.jpg
                    - event_83b24e74-f3df-4040-8ea0-e188d9898424_1755090418.jpg
                    - event_7393650c-e2e8-4553-ade2-3b13d332ce0a_1755087479.jpg
                    - event_491c14e8-40ee-4777-8a3b-97306f14cf99_1755090511.jpg
                    - event_716e4288-4d78-4b72-a6d5-1a14cc73ab10_1755089893.jpg
                    - event_75b88427-8145-4c91-b4cc-4430b9502c75_1755087408.jpg
                    - event_a0b6f011-aa67-40d0-863a-423f80a55f91_1755089382.jpg
                    - event_692148e2-d636-46f1-aeed-16934f19b451_1755085930.jpg
                    - event_d757bbd7-678f-4c5e-a776-e959ef23329c_1755088208.jpg
                    - event_53fce0c9-5731-4559-bc77-7ed944c0a52b_1755085496.jpg
                    - event_40c1a62c-bc05-47ec-81d8-dd4f0a949c34_1755085086.jpg
                    - event_b249621e-7d3b-47c7-977f-e1653aa3fd43_1755091038.jpg
                    - event_70be8b5f-1d64-4ffc-bd9c-affa2dc097cc_1755086685.jpg
                    - event_fd9711a9-364a-4889-a909-35b63761e450_1755085003.jpg
                    - event_f51ed204-93a9-4fa3-afee-697e42701f29_1755085607.jpg
                    - event_da5697ad-951b-44db-9571-875ac5324936_1755090460.jpg
                    - event_cad03fbb-37d9-4793-9855-901f62c676d4_1755084811.jpg
                    - event_967d149c-808b-4bf8-8985-1e20370f9b9b_1755091642.jpg
                    - event_8d65ed1a-f0e3-48fd-a501-704712ae212b_1755091237.jpg
                    - event_1f4e6e10-6ea7-4378-93ef-1f12d64675d3_1755084552.jpg
                    - event_bbb4ec37-d263-4992-b868-33fb46c192e0_1755084666.jpg
                    - event_504bbdd4-279e-476e-aa89-1e2a86332c30_1755082800.jpg
                    - event_bb8d9faf-ead0-4011-9f67-dca95bb1081e_1755089937.jpg
                    - event_e32f8cd5-b0dc-4734-8137-475c19c0d74c_1755087137.jpg
                    - event_d71bba51-2d8e-4d6c-a906-9854ac7e6429_1755084778.jpg
                    - event_61885e45-8caf-47a9-995f-ae274b826c85_1755089090.jpg
                    - event_8a0f662e-ce46-4a68-8f3b-43c30526894b_1755089588.jpg
                    - event_ac894d4d-4057-4c8b-9ab6-cdf4e2e98494_1755090540.jpg
                    - event_40d33009-5e70-47c7-94b4-10d412513430_1755091337.jpg
                    - event_f8cc0756-4464-4680-9b0f-c6c675af8a1f_1755086373.jpg
                    - event_6a2c4707-7aa0-4103-8b69-12695f9973a7_1755084505.jpg
                    - event_ed3b82c4-66a1-47c8-9ffe-2ef074182c1e_1755090580.jpg
                    - event_14da8a89-2e5d-4d66-9231-b00f643bf02a_1755084867.jpg
                    - event_02d92960-50db-4750-94a0-d2e007135a4a_1755086656.jpg
                    - event_000ad928-8705-41f1-9627-e7dbaeb8cfcf_1755085598.jpg
                    - event_2e41f733-9a99-411b-9b55-3da70a981d30_1755088055.jpg
                    - event_22be93b6-a8b7-4a01-81c0-dba73615d3cf_1755082743.jpg
                    - event_063fb191-8a93-489c-ada2-8cc44f6844a4_1755087048.jpg
                    - event_86fe1c14-2e48-4c23-859f-b3878b6d2aaa_1755084476.jpg
                    - event_d83229ea-7b8f-467d-8b90-ef1a21a454f3_1755086208.jpg
                    - event_d706735b-7069-40da-91bf-21905fdcc9a7_1755091522.jpg
                    - event_c4c8412b-f41f-4558-9e97-29659a6526df_1755084902.jpg
                    - event_369dabad-a181-4b1f-93c4-1c33f2780ce4_1755085062.jpg
                    - event_3f47d904-20a2-4efb-951f-19dcab212230_1755088147.jpg
                    - event_649a86ca-fd7a-4609-b503-c5e1650c5e04_1755087252.jpg
                    - event_fb1c6dc3-3c63-438d-a33b-589bc98fbd7c_1755087959.jpg
                    - event_b5546c51-7c73-464c-9fdb-a1137a02c722_1755084617.jpg
                    - event_3003b13d-539e-4687-9d7b-936646ae94e3_1755084965.jpg
                    - event_1c01b3f5-08e3-4fc3-8294-ff7b503e4151_1755085150.jpg
                    - event_64fb76f6-8421-4ea7-9e83-f5309710c209_1755091411.jpg
                    - event_352d3bf1-7015-40de-b0c6-f1cdc9322854_1755086579.jpg
                    - event_db513ffb-8923-43bc-956a-1690c84d44e2_1755086891.jpg
                    - event_7f73eb5a-674a-4970-971a-a6ed1442a21d_1755091789.jpg
                    - event_55954cb1-6bac-466c-b5a1-c06946ca5c0e_1755089955.jpg
                    - event_59c59934-4bd4-4191-a3bd-d36972be4422_1755088175.jpg
                    - event_233e7d38-10e2-4e0c-84d2-42141dc06ec4_1755090960.jpg
                    - event_585896d1-b417-4f23-bbbe-fc53f1d6443e_1755086682.jpg
                    - event_c2ea0129-1a7b-4ed1-8f20-ba2cb2a8cd7e_1755089166.jpg
                    - event_837c1e6e-e921-4e94-9181-8f174d82ccb7_1755088922.jpg
                    - event_a31b5f77-fe33-492b-be45-b50286b1820a_1755084930.jpg
                    - event_8e883345-0b8a-4f8f-a451-dd7392d39294_1755086071.jpg
                    - event_3bfd3496-5be9-428c-941c-4e652b666bc2_1755084792.jpg
                    - event_30fc56ee-463b-4080-8d65-f58e1de1e94b_1755083339.jpg
                    - event_86f0d8a7-c90e-45ba-a96f-3609b3fd25f0_1755086659.jpg
                    - event_b226ae72-61d9-42da-826c-c3f2f1bdd45e_1755082582.jpg
                    - event_361f0007-0521-4df0-9a17-28e229a60c73_1755086598.jpg
                    - event_68470449-2f6e-4e55-b8a1-a912500fb471_1755090182.jpg
                    - event_bbc87210-afaf-4794-ad06-22aebb85208b_1755091665.jpg
                    - event_63871bdd-2dbd-4d62-919e-d6d6bcdd23a2_1755086973.jpg
                    - event_37ce84df-8b27-4e03-8b57-a5e37b6f5bcc_1755090968.jpg
                    - event_796e36e2-bd85-43c3-b97a-9f581213543e_1755091480.jpg
                    - event_4c76dd8d-03b3-4784-8a91-8f12fc45b597_1755090268.jpg
                    - event_7bc71342-e416-448f-8eb5-911332aaa746_1755083447.jpg
                    - event_4fa431ca-b9e2-4af6-b1f0-e84d1ac9f6a2_1755091673.jpg
                    - event_f1e3d4b5-ca4e-4d8d-bd93-9503960ede30_1755085122.jpg
                    - event_881876fb-4ca1-4484-892b-6ffe93d7ad37_1755087384.jpg
                    - event_3a0a5125-ca67-47dd-a1aa-bc5eb4113b67_1755086442.jpg
                    - event_810e4f95-d53d-49d8-8ab1-2bc25f0ba85f_1755090211.jpg
                    - event_2db6cf98-1304-4746-b830-eff0bb37088b_1755087741.jpg
                    - event_29a0cdaa-1aca-4525-9d9f-43a5920a3cee_1755091373.jpg
                    - event_59321cbf-06d6-43a3-b65f-087249e9a90e_1755090442.jpg
                    - event_19dd00ed-c1b7-46c7-a26d-eaeaff25bf97_1755085033.jpg
                    - event_57b7eded-5ffe-4321-899d-686ed35d7fb5_1755087172.jpg
                    - event_f0676edc-03e5-4f75-9048-dda51d7d7c40_1755082557.jpg
                    - event_b4d300a3-c00c-4504-b9a8-3c0ad385fa9b_1755091768.jpg
                    - event_b1230cdc-cb46-46f6-9893-91756d8e6933_1755089885.jpg
                    - event_12ffd8c9-482a-4692-9e81-87a9142fe2b7_1755084863.jpg
                    - event_f4d720b6-021b-4205-b309-d482f8d2bd8e_1755085943.jpg
                    - event_552157c2-e9e4-43ca-8f85-dae4e33ff7a9_1755085871.jpg
                    - event_9cfa526c-22f6-4e22-90f5-56b7f4d8cecc_1755087685.jpg
                    - event_2bda9487-2c18-42f1-ba78-b04855f7b450_1755092155.jpg
                    - event_716c97f8-6f2b-49f7-8b7b-282529a4d3de_1755086924.jpg
                    - event_6554ddd0-a61b-4ba5-bdb2-c7b880bc0ad8_1755091019.jpg
                    - event_70db9f8c-4444-4deb-b25e-61e68bab827a_1755091973.jpg
                    - event_070e5a83-e29d-40e9-9251-048b1b5a8ee8_1755084588.jpg
                    - event_7f638149-d828-4fa1-b159-5bd4a3772412_1755087877.jpg
                    - event_1b1d9b91-9dbd-4403-b510-6d1208736ae2_1755091842.jpg
                    - event_62aecb81-6aca-4b6b-829b-d5b4c922b42d_1755082717.jpg
                    - event_f380c64d-5349-4eea-a40d-fcfe9544fd48_1755084560.jpg
                    - event_a4709e8d-1776-4bd7-8248-9a2ead2ea099_1755087832.jpg
                    - event_beb704aa-1951-405c-914a-4acb86981949_1755087809.jpg
                    - event_0f62ecf9-5e18-40c6-aea3-76b7f1e2e541_1755084855.jpg
                    - event_fba24c9c-bbe6-43ec-81da-ba11ea489f0a_1755091893.jpg
                    - event_fde99a42-3af1-476d-b211-278f99e507d9_1755086980.jpg
                    - event_62fe970c-0c33-498d-b050-5d202a9323d2_1755086018.jpg
                    - event_524b5234-893e-4e20-8536-c8d419d43a68_1755089047.jpg
                    - event_d6b42641-e05c-4ca9-b9ec-6e60d865ff8e_1755087864.jpg
                    - event_7729b864-e7e2-4e36-a11c-54fcef324102_1755084940.jpg
                    - event_c50bef3e-44dd-4315-bac2-b13d253ef84e_1755083981.jpg
                    - event_3c0b33f8-f8e6-48a2-9f7e-810506a39c13_1755082670.jpg
                    - event_f9375e77-b672-447d-b36e-37e6160a99ed_1755087364.jpg
                    - event_e10e6a58-5f63-466f-8335-44d185d1e389_1755087891.jpg
                    - event_d0a55e81-bfc8-476f-b3d0-a4d708ebd2f1_1755087759.jpg
                    - event_c00bbaf4-71ce-4de4-bd40-6ce3e4b7d4cb_1755087459.jpg
                    - event_2e5d27c7-5303-4cfd-90d4-f9589868b376_1755086353.jpg
                    - event_b79cd4b8-a939-437d-84ad-0a5222cb4f79_1755087718.jpg
                    - event_ccb22f25-41ee-4547-b984-5bba3b773101_1755085476.jpg
                    - event_a826ee3e-33b4-40c1-87c2-96839e59d01d_1755087789.jpg
                    - event_6d9e2107-6ff9-4ba8-8a78-17440721cdfa_1755092009.jpg
                    - event_44defb5b-827e-4d48-9c9f-0b8c636318bf_1755087675.jpg
                    - event_f7b97942-92fc-4815-9136-b0c2a397e82f_1755091737.jpg
                    - event_5b3ad08d-8337-4c8e-97ea-9c0faf0b607c_1755084142.jpg
                    - event_1495e1c2-2301-45ce-acd1-bc561ed1eb1f_1755086022.jpg
                    - event_f9b97ba4-975c-4f39-919b-3c9d2c3c9dab_1755084876.jpg
                    - event_32934105-f4ff-48f1-a949-bf37a54e10fe_1755091694.jpg
                    - event_137b9f4c-b48f-4072-8555-ee2246fbdca0_1755087333.jpg
                    - event_1e69bc98-57ab-4e31-b3ec-e2f264b33c03_1755087859.jpg
                    - event_7d2435a3-9e26-4c0e-a0be-1ef41acd3bbe_1755092242.jpg
                    - event_9794676d-de73-4a91-a7aa-07eb83452707_1755089614.jpg
                    - event_1a796b9f-561f-44b2-97ae-a0f82436ad1a_1755085635.jpg
                    - event_4497647b-5e78-42b1-9f0f-766e478d0dc4_1755090520.jpg
                    - event_8ffb48e8-cb2a-4764-bc55-e9392a9661a5_1755090136.jpg
                    - event_8e80b275-f348-4c9c-9773-74dbb4720ce1_1755085113.jpg
                    - event_803d0c80-264c-493c-bd83-2928aba8d8f2_1755086092.jpg
                    - event_874de4fd-bb57-4b5e-b738-4f826fcc6b30_1755084680.jpg
                    - event_d2a1421f-e076-4b2b-91dc-f7687880496a_1755091163.jpg
                    - event_bf8909d2-245a-4fc1-934a-62717502b8cf_1755082502.jpg
                    - event_1275ad7e-e496-4e7b-b0af-72dfdad461fc_1755084158.jpg
                    - event_8c6295cc-8967-4d63-b723-7cbac1f1e49f_1755085116.jpg
                    - event_8a11261e-7f6d-4f13-8730-deaad944c46e_1755088192.jpg
                    - event_0d01503e-19a2-4635-aff3-8311b926e52c_1755088133.jpg
                    - event_a21b3277-25fa-411e-8d89-58be4bc21c89_1755090503.jpg
                    - event_52016d50-401f-4433-a452-52ce10cfa599_1755086051.jpg
                    - event_e2d1abdf-cba4-4182-8ca2-8f913cf82006_1755089212.jpg
                    - event_8bca653e-defe-4e67-8d87-075e4c628283_1755085554.jpg
                    - event_91931e39-1d6d-4e23-bb30-9b04eda28bdb_1755087990.jpg
                    - event_e3786ff6-cf7f-4070-b16e-4376fe584850_1755090824.jpg
                    - event_7ab4ac78-a4c0-43c6-8b8e-28dc742fc874_1755085596.jpg
                    - event_33477c34-8e50-47d5-92e3-52292ecdd30b_1755085925.jpg
                    - event_24539cca-d2ba-4ca9-a9a5-3cbec07dffbb_1755091063.jpg
                    - event_f233ae35-c5f3-444d-a895-5c5f597a449e_1755089821.jpg
                    - event_c22de935-68bf-4e10-8d9f-0e13d7725995_1755082754.jpg
                    - event_dd87f393-a44e-4f9d-9b91-8a2625cb0799_1755085934.jpg
                    - event_9273c13d-df5e-4744-aa2d-2eaa1670d2dc_1755087871.jpg
                    - event_88746579-d28e-4a64-873e-ea744f1c6013_1755090270.jpg
                    - event_6a145cf8-3a47-4eed-9d27-53c62e33e1be_1755087354.jpg
                    - event_a7a6946b-f68a-4bd1-ab10-e8d72d4043a7_1755084578.jpg
                    - event_6965368c-cf9e-4dae-bc12-e277a97a56d2_1755090536.jpg
                    - event_83a956bb-65b9-48d5-9e65-b67a490487bd_1755087701.jpg
                    - event_fcc3a287-0eb1-4ebd-864e-65f3e8e1ece4_1755091569.jpg
                    - event_682dd681-abe7-4ec9-b71a-35475bdb59ac_1755084661.jpg
                    - event_c3d7e548-77b0-446f-b891-97db2e184d71_1755084879.jpg
                    - event_68e9e11f-ac23-46df-96d9-fd3871b69d0f_1755085024.jpg
                    - event_60f56222-8231-4f9c-bc90-fcff04f890d8_1755089610.jpg
                    - event_9baee9e5-bb9b-4b5b-b887-a16de7c713e9_1755086214.jpg
                    - event_1e679a59-aea5-474d-94f9-ae0f0e20c7d2_1755084782.jpg
                    - event_df0a83b5-77f0-47cc-9686-bf04e830149a_1755090217.jpg
                    - event_808b9d5f-617b-4738-8a8c-27e523f59729_1755084814.jpg
                    - event_43596df8-8707-4370-b982-73c9c73266d3_1755082499.jpg
                    - event_e3816e67-558b-467d-aaff-b69ea5550551_1755089376.jpg
                    - event_3df2dfb9-a474-4513-a06e-c5a0a7162b9b_1755087199.jpg
                    - carry_bag_images/
                - usb/
                    - qc_7ba49d51-5914-487d-845f-8bf170ffed01_1753993619.jpg
                    - qc_36c499b4-5195-4231-a4f6-bc3c3c7fd9dd_1754062622.jpg
                    - qc_02743af3-61e6-4615-9b55-cea02af40fe7_1753993060.jpg
                    - qc_9612c018-4a07-44fe-8e74-dec3404de104_1753988446.jpg
                    - qc_e8c6c4e3-6e52-4cf5-b1ff-7a6e984113e7_1753988479.jpg
                    - qc_e7f8c919-316f-4c9c-b524-b16431a6c213_1753993189.jpg
                    - qc_e88c82f3-f287-4f27-85ef-148adcdffdff_1753993135.jpg
                    - qc_4a52d3d0-d00c-4fa0-b502-1c9fe2751135_1754155059.jpg
                    - qc_da777522-01de-42f9-88fe-606aef7ae151_1753992745.jpg
                    - qc_b55e2464-05a5-4092-8841-039aa29ca514_1754059727.jpg
                    - qc_505184e8-5818-45b3-9773-8f5cd59e3c3b_1753988832.jpg
                    - qc_151ca5c4-ff84-4241-a436-904ce6f2117c_1753993319.jpg
                    - qc_68d3a0ad-fc7d-45e9-b56a-579911ea0360_1753993512.jpg
                    - qc_7cf390c3-517f-4628-84f8-8e0e66b405e1_1754153398.jpg
                    - qc_4c679977-727c-4777-9e03-ac943b40370d_1754057384.jpg
                    - qc_adfee187-7d7b-4b81-875a-1e0805601695_1753993211.jpg
                    - qc_1982fac9-354b-4f2e-8fe0-e73ff3e4cc22_1753988568.jpg
                    - qc_03c30ebb-922c-4ce6-a0e3-d2db9a691749_1754092034.jpg
                    - qc_e35231b2-9362-46d1-ad4f-53a0320036a4_1754091984.jpg
                    - qc_95177f37-df36-4454-800e-78ae864ab40f_1753993480.jpg
                    - qc_5e9f16f4-659d-4fb8-a4b5-18e6158f4990_1754082189.jpg
                    - qc_142720cc-04b1-4e2e-909d-da6b1c2ef7b3_1753990489.jpg
                    - qc_e26842c7-0049-4760-9b19-6a9a2faf9751_1754092095.jpg
                    - qc_7c77bc3c-0bc5-4e9f-889e-193f49afb455_1753992570.jpg
                    - qc_a675103c-95f5-49a3-a395-5484af9817a0_1754094030.jpg
                    - qc_a9445fff-8eea-4e6a-b7d5-fcfb66b94cff_1754155320.jpg
                    - qc_7907ce78-3460-45b1-ab02-fd7f5a31d86c_1754057083.jpg
                    - qc_e06014e4-f5e4-4e28-807f-c7e9ba2e63b4_1754153351.jpg
                    - qc_328f65a0-1dcb-4129-9bef-9a01f087166f_1753993940.jpg
                    - qc_207ac3fe-ae3e-4329-bee5-7d67cbf09997_1754082831.jpg
                    - qc_b4b54798-ebb5-4d7a-8dd9-ffa378b8a25f_1754091950.jpg
                    - qc_5d5378f4-cc9b-4de1-8a6b-dfa3901fd296_1754074693.jpg
                    - qc_b794daca-e385-46e7-b03b-966682fa01f2_1754081871.jpg
                    - qc_c2a66960-3204-439a-9169-5513239da4e1_1753989018.jpg
                    - qc_0cf2c7ef-5cab-4974-a283-269d95f776a1_1754064313.jpg
                    - qc_5c0d45e0-b581-4bd1-accc-2ff82e3d1bdf_1754091939.jpg
                    - qc_93a991db-9828-45fd-87b0-446534c05cc4_1754081641.jpg
                    - qc_438f43e9-d0e7-40ed-850f-e31215636453_1753992800.jpg
                    - qc_431efb0c-37f0-4915-87e3-76845858400f_1754057005.jpg
                    - qc_7c561440-af1c-4fa8-a389-2d5670448191_1754153473.jpg
                    - qc_2238b6fe-e455-4f1f-b00c-d17db3e7212d_1754081574.jpg
                    - qc_aa83fa4d-7db2-45a2-83e9-7ed90e5bc414_1754064309.jpg
                    - qc_4ff97e20-e270-43c5-81ef-23afa1306a9f_1754089003.jpg
                    - qc_f4fa1f26-cd47-4522-8bdd-f6995a920f22_1753992767.jpg
                    - qc_cff3d032-c7ff-4c8a-b846-8d0690a38d19_1753992389.jpg
                    - qc_2084c1f1-bf7b-478e-be77-dd8d87bf365d_1753992581.jpg
                    - qc_abffee04-89a7-47a3-8fac-b312f1860f62_1753994217.jpg
                    - qc_5345d75a-7481-40e8-bbb6-7ec61f8b3960_1754064318.jpg
                    - qc_ee9e8033-5b70-4089-b31e-d6c39e5861fb_1754057376.jpg
                    - qc_0d713a14-3337-495c-be34-87f196ec103c_1754059824.jpg
                    - qc_39752bca-3a42-4878-9993-a88c9a8f293a_1754155100.jpg
                    - qc_3484adca-9ec4-48a0-add2-be5360be1599_1754059807.jpg
                    - qc_2bce7506-3795-4046-95e4-80626b7f56c1_1754070947.jpg
                    - qc_6bc5566c-1d6d-4223-9121-d5b446f54d7f_1753993157.jpg
                    - qc_d79beed0-d733-4ee8-9a3b-406e3af963f0_1753988920.jpg
                    - qc_65150c3f-5be2-4d7e-8383-8cb397ea12ee_1754074670.jpg
                    - qc_87b6a047-cdc2-433d-92ed-d394e78290de_1753992010.jpg
                    - qc_6cca963f-1521-41fd-bb88-6e169551079b_1754049196.jpg
                    - qc_7c7e2763-3b3c-47e2-973b-2b91aafc5a98_1754074579.jpg
                    - qc_766de91f-07ef-4357-8eea-9436e4102895_1754070923.jpg
                    - qc_2653236d-5a5a-456f-b354-93385642772f_1753988546.jpg
                    - qc_449cc7b2-12e4-48ad-83e8-5b17cc690673_1753994185.jpg
                    - qc_3dc7fd2a-ab1a-4fa0-b875-e475687f29ba_1753992548.jpg
                    - qc_312fdb83-56e3-419f-8d74-65d285580922_1753992378.jpg
                    - qc_a97e0aa1-0eaf-42b8-9018-68ad2f51e9c6_1753993972.jpg
                    - qc_399af6d0-4b82-418f-8c6c-2baa8523fa43_1754081314.jpg
                    - qc_9aebefd0-f48d-445e-a317-c070b89381d2_1753992723.jpg
                    - qc_99427d56-73dd-4540-af9e-874f4e6d0d80_1753993049.jpg
                    - qc_79e5c9ec-8776-488b-8a1e-428966e386f1_1754059849.jpg
                    - qc_a1bbb6bc-9f6f-40ea-90dc-cca80b7d3056_1754091135.jpg
                    - qc_542d5676-e0e3-4dcd-ae31-4b230efa4c3e_1754070953.jpg
                    - qc_5c18f456-2845-4b33-8dd4-86c61c4b4c42_1754092017.jpg
                    - qc_0c9ce159-86fa-4cbc-b759-ef126c3f86c7_1753988745.jpg
                    - qc_df9dcf1b-b15c-4453-a235-f233c267b4aa_1754081838.jpg
                    - qc_061c2bfd-c506-4601-b8df-6c68b8dc4b9b_1754082178.jpg
                    - qc_b37deb02-35af-4991-b113-f60f7bf19967_1754074682.jpg
                    - qc_26c1f056-c3e8-48f4-82ca-e8e80166a660_1754081336.jpg
                    - qc_588225f8-04c2-49f9-b4b6-59923eb97679_1753992952.jpg
                    - qc_e959ad10-9dab-4d0d-b05f-97ae65fba90d_1754059671.jpg
                    - qc_6269d150-4666-4aed-bb27-0bcb6d05cf0f_1754071206.jpg
                    - qc_f1db004b-9462-4b88-9077-c9c9d74a7fb6_1753992843.jpg
                    - qc_3a076602-a884-4a80-babd-6ff2264cf60e_1754081347.jpg
                    - qc_9caf2016-664f-47f7-bc42-ec8449b2908b_1754081618.jpg
                    - qc_45c61868-b0dc-41fd-9f34-cb5f74c715cb_1754062632.jpg
                    - qc_46e6b3b0-13dc-4a84-8b0c-2d7a1b6cae78_1753992367.jpg
                    - qc_d123b3db-6d27-42e1-bf4a-ca94b53d855f_1754064436.jpg
                    - qc_8de877be-8005-4670-829b-12e852dc1f9b_1753993609.jpg
                    - qc_9eaa512f-8733-41c3-864a-329097222735_1754059736.jpg
                    - qc_de3d8364-0add-4656-bf82-07ef19cd9ccf_1754064316.jpg
                    - qc_d63d537e-564e-45b8-83c9-dbf2cd29f38d_1753988953.jpg
                    - qc_6710298f-67ac-486e-991a-354fd8a1a5fd_1754071195.jpg
                    - qc_07a48cea-e761-4298-82fd-fae2b9c994db_1754064392.jpg
                    - qc_7953e00c-58e2-4f59-96d8-6306698ec9d4_1754155536.jpg
                    - qc_4e8fc9cf-9329-4cd3-ab98-852f4f1de9a8_1753988964.jpg
                    - qc_673e139e-d0ab-4eca-b63a-4e0a7e169103_1753994090.jpg
                    - qc_6fd4bd50-795b-4875-905c-340cd142674e_1754088958.jpg
                    - qc_23b1d30f-5afd-4e86-b920-a80604d521ec_1753988612.jpg
                    - qc_0575d2cd-c900-4aec-8ecb-22d676019101_1753992789.jpg
                    - qc_a2e9a0ae-d19e-45e4-ab2e-24ab373cf4d1_1754057383.jpg
                    - qc_5120c2b0-9bbe-4128-9b1e-11d56173be53_1754081775.jpg
                    - qc_c8a0cb9b-5642-4904-ba08-2a88d5703b5b_1754093865.jpg
                    - qc_ea204859-38c4-45fa-9618-f2f17ab7b96d_1754081894.jpg
                    - qc_1e9c4fb5-545a-4aa6-b5c9-6fbf46d5f3e0_1753988435.jpg
                    - qc_58fd62b2-74e8-401c-897e-21b6cd07043a_1754057101.jpg
                    - qc_ce75aa0a-3b09-4274-a11f-40a5de036756_1753993576.jpg
                    - qc_6803356f-54bf-4dc7-ad78-d5b988d101f0_1754057379.jpg
                    - qc_80a5e03e-0306-4e52-b12e-a7f5054ceff2_1753988601.jpg
                    - qc_60232c99-87b7-487b-b05e-c74a9b22dbcf_1753988986.jpg
                    - qc_e83aeeb1-8b93-42f2-8e37-e688fb383bd7_1754082559.jpg
                    - qc_f0caed6e-88dc-4db3-9880-20b57c0136c0_1753993233.jpg
                    - qc_5f610717-883d-469c-b65d-7a72e075f53d_1753994111.jpg
                    - qc_11bbaea3-a415-4130-b19e-45bf095b8dae_1753993071.jpg
                    - qc_34a29c6f-dfad-484b-8024-0e2e22ba24fd_1754057409.jpg
                    - qc_a77a8d2b-a941-4ab4-a462-4d258cc035fe_1753988844.jpg
                    - qc_b821a1d5-6169-4b14-aa82-11baedbf2219_1754091889.jpg
                    - qc_9dc0584b-6344-4046-b17c-fb6c2853df74_1753992962.jpg
                    - qc_10441048-e8f5-4906-b5ee-5cec6687d5ca_1753988756.jpg
                    - qc_dfeb0bb3-fdc1-46df-94fd-cfe120b1bdab_1754088970.jpg
                    - qc_6e0eb092-6eb6-4516-913a-83b8457cf8d6_1753994175.jpg
                    - qc_fa8e5e18-b439-4a38-a825-d0bfe78554b5_1753993929.jpg
                    - qc_ef5091d9-e258-4bac-8bef-436b3bbc7f14_1753992973.jpg
                    - qc_1969a648-917c-42dc-b012-04271e12f79c_1753993630.jpg
                    - qc_abfe9f44-e109-4805-99c3-930834445c87_1753993415.jpg
                    - qc_8b951d4f-f31d-452d-9c80-cb0e82e161cb_1753992734.jpg
                    - qc_cf4b2717-e047-45ef-9216-b2ec670c7ca3_1754081652.jpg
                    - qc_4634c127-86ab-4088-9ad7-734876fd0420_1753988634.jpg
                    - qc_02b9d825-f99d-403e-9829-477f457a6ae4_1753992422.jpg
                    - qc_74b96831-dae1-4fef-95e1-d39227207f8c_1754057294.jpg
                    - qc_8d764ae6-8e9d-4b91-ab05-25de1f70f3aa_1754094054.jpg
                    - qc_cdc8f155-04cb-4574-802c-e7b15ff55934_1753993276.jpg
                    - qc_79a2ca73-c8a5-4f52-9a93-e1cbabf7d41b_1753993673.jpg
                    - qc_604eb7da-e4d1-4c24-aca6-f679f7a759dd_1753992854.jpg
                    - qc_6d26fff8-2078-4e39-bad2-1c0d8c03c2dd_1753992603.jpg
                    - qc_9a54bde6-2313-4d08-93c1-a8cc1fb0ec61_1753993383.jpg
                    - qc_1ef65eda-a620-488f-b13f-171dc6db1b47_1753993855.jpg
                    - qc_3d0e0cb0-f721-418c-b39c-9bfd8123210f_1753992493.jpg
                    - qc_4568e0a9-235f-48c6-971a-259549b94a6f_1753993168.jpg
                    - qc_3ec2ce5a-0c78-4dc9-a8c7-41a2cf8b06a3_1753993983.jpg
                    - qc_24552f5d-fa65-4882-8984-80561b771fab_1753992261.jpg
                    - qc_1f9db3e4-7613-4077-b948-84f9b35ff82a_1754071182.jpg
                    - qc_04a958dc-3154-4885-8c5a-a1e2f7a505d7_1753988909.jpg
                    - qc_b4a0d818-232f-4a51-ba09-b86863e3924b_1753993908.jpg
                    - qc_88bedad2-f663-4090-b8f8-9413a9973fb3_1754155168.jpg
                    - qc_f69be23a-6f69-4485-8fb7-828d3cc341bd_1753992984.jpg
                    - qc_d64835b9-3dd7-4963-a5f3-42fee2ccc999_1753988501.jpg
                    - qc_4683c897-b93f-4e91-b447-df334f6af049_1753992647.jpg
                    - qc_8041d16e-9dfc-44ad-8d7d-66170ff9682d_1754153477.jpg
                    - qc_8e3924e8-9706-4b00-b6c0-2c1af1c17acc_1754081596.jpg
                    - qc_3fe6ad86-c865-4519-8f81-bf5bbc6d585b_1754080597.jpg
                    - qc_dfacf945-43c0-4095-bf51-e0593c3cf64e_1753988898.jpg
                    - qc_d7e43b80-b5b7-4b28-a3d5-85b7bae004a2_1753992515.jpg
                    - qc_5a07b0c6-ce4a-4862-a3ac-aee9b89cce03_1754094065.jpg
                    - qc_70de5ba8-b3b4-4448-9b13-8ffe5b77932a_1754081753.jpg
                    - qc_14e97584-b40e-47d0-a76d-989a5e0361dd_1754091901.jpg
                    - qc_e2e9ae3e-ffa3-4842-a30f-2112f0537cfb_1754059841.jpg
                    - qc_a4d95fd0-bc9a-4a78-aa90-9cc27e348f59_1753993329.jpg
                    - qc_9c60f05b-3533-44ae-8825-eb623bd03240_1753988390.jpg
                    - qc_65c6f47a-20aa-4759-955b-db2ba668f940_1754057082.jpg
                    - qc_7d2a9cd1-6304-4e22-b37c-5b1f6e05f080_1753991097.jpg
                    - qc_b7b106fc-44e1-401a-8930-699af3505fd1_1754154934.jpg
                    - qc_87333c67-03aa-4c27-9643-004384c06723_1754057026.jpg
                    - qc_c968c331-9a43-41cc-b3f3-ce6dfd6b852b_1753993103.jpg
                    - qc_c6a39db3-4c2e-4c1b-888d-3586018187ef_1753988678.jpg
                    - qc_968d25b2-af7d-4d4a-86d3-425533d8ecb8_1753993362.jpg
                    - qc_1f888be8-68e5-4f59-94fd-95eba16c1eed_1753992411.jpg
                    - qc_5cb23902-cb47-450c-a8b3-3b6fa5e1e5e5_1754091867.jpg
                    - qc_98387f96-fde7-4bc7-a40b-9f244d339119_1753993919.jpg
                    - qc_02cdef81-b911-405e-9047-71f41e416fc6_1753992680.jpg
                    - qc_e727ec36-7b8b-4bc1-afc9-63169aca8307_1754057021.jpg
                    - qc_7b204244-3d9b-4bd1-840e-ff7dc97e9964_1754089015.jpg
                    - qc_41138e8f-2cdd-4817-b2d0-bf961c316ad1_1754155015.jpg
                    - qc_00c7b2b6-d22e-471d-beb4-1e4d752fa14f_1753992504.jpg
                    - qc_3a24fe50-f95d-41c8-a9b3-8007ec5943b6_1754091917.jpg
                    - qc_4da0a772-9893-415d-8c24-83f1a46b41e5_1753994143.jpg
                    - qc_3dd5fdb8-cac1-434b-84fc-87b166bf7628_1754155499.jpg
                    - qc_ed585a2c-3aff-4b9b-8afc-88866561587d_1754064316.jpg
                    - qc_0ddee116-f3e0-42b6-bf4f-2a2ffe8c2252_1753994196.jpg
                    - qc_02ff2db6-a568-4b33-aeb2-1f1d6d7679bc_1754153480.jpg
                    - qc_5b606e3e-c170-4280-af70-b5eed258d883_1753993426.jpg
                    - qc_503172eb-cd06-4393-8e7c-ab50978b34ca_1754092107.jpg
                    - qc_8567e27b-0b4c-4b0b-a8d4-25f9252b61a7_1753992482.jpg
                    - qc_58b924a5-b892-45d8-9df5-c7bb2ac34df6_1753988457.jpg
                    - qc_eb31c61c-9ed2-4052-838a-6185b41fb539_1754091878.jpg
                    - qc_05c3ef42-92c2-405e-b433-958be9950004_1754074648.jpg
                    - qc_b9bbcc3c-cb1d-4322-97a4-05201ad8f0d4_1754057027.jpg
                    - qc_8001b47b-37ab-4156-88b8-0d43abc5cab2_1754081325.jpg
                    - qc_e932af10-4e82-4b70-8dc1-3986ef172f88_1753990478.jpg
                    - qc_2eab298a-0212-4b56-b260-9aa3942cf38a_1753992658.jpg
                    - qc_c7e8c456-51f5-4b01-9dfa-c59ee1fcf989_1754155479.jpg
                    - qc_ba430841-6747-40c2-9161-bacc71989712_1753988887.jpg
                    - qc_22bfc254-34b2-472f-83db-c1430467f303_1753993780.jpg
                    - qc_84dd537d-202f-4ab3-8ad4-46a6cecb4972_1753993748.jpg
                    - qc_ed549df3-df57-4f31-bf59-dff8116af0c4_1753992444.jpg
                    - qc_d89aa674-93e1-4eea-9629-c586e2d40110_1754057085.jpg
                    - qc_a5384126-301a-4e11-87fd-6c014c6e3a85_1754070935.jpg
                    - qc_5dc2ba0a-484d-46b7-902c-746dc91e3781_1754155083.jpg
                    - qc_72e53485-d717-4968-9ee3-926345998c6e_1753993833.jpg
                    - qc_b87c795a-96bd-41d8-a945-ffbf5ffd7b58_1754094043.jpg
                    - qc_ad593a5c-ae63-4c70-8f8a-81498a80c34d_1753993448.jpg
                    - qc_504c000c-1fc3-47d3-bbd8-e4664115ce2f_1754056999.jpg
                    - qc_6b4f44bc-dd4d-452f-b2d7-66f151a6aa90_1753993340.jpg
                    - qc_bfe1c856-1af8-4dcb-acd8-880c1fdfeab3_1754064442.jpg
                    - qc_b02dcf0b-400b-44b3-a1aa-63a310220ae9_1754153466.jpg
                    - qc_3c8f24e4-354e-47b4-8848-8b0b45756888_1753992592.jpg
                    - qc_fb9a8ee6-0b47-4670-b49b-8adbc2f3d578_1753988579.jpg
                    - qc_ccdc7013-218d-49a4-af06-9ba8f1e42e6a_1754059661.jpg
                    - qc_f93176a0-0db1-43b8-adb5-783fe55b5f70_1753992118.jpg
                    - qc_06175f3a-4600-43ef-ab65-fa43dfb12c62_1753992334.jpg
                    - qc_3646ddd5-eb47-44c5-ac60-3f0a7bd2973d_1754070772.jpg
                    - qc_c709e5b3-6e12-499a-a284-ad9b0ba7c240_1753990510.jpg
                    - qc_1fe84ca5-240f-4ba1-8c9a-53da74051673_1753992897.jpg
                    - qc_2ccd7677-700e-472e-9afe-b133aa688ae0_1753993038.jpg
                    - qc_85b6bdf5-6404-49c3-8461-9f231b5cb3c5_1753993351.jpg
                    - qc_e55169a6-0c87-4e35-a026-3eec7827bc23_1753993769.jpg
                    - qc_de6e1405-d3e8-4732-8001-7cb27e6d6f54_1753993125.jpg
                    - qc_42ad3665-1e9f-4821-84d6-90fff1d8eb66_1754091845.jpg
                    - qc_7d1ff317-a73c-40dc-b35b-058895c18ccc_1754081882.jpg
                    - qc_4df8f27b-9a5a-4ddd-8d56-ad6f010acec8_1753992625.jpg
                    - qc_4e2b0e86-0910-41b7-b89f-45997ba220ef_1754153391.jpg
                    - qc_ddb45958-1105-4741-8a11-260a1a74d209_1754153420.jpg
                    - qc_c1c1e58c-1d34-4fa6-aeba-59a50c62571c_1754059834.jpg
                    - qc_247cc7ea-09cb-4d41-92e1-399bbf1b1cf8_1754088992.jpg
                    - qc_45723bf8-d8ba-4d65-a6e7-3bbd3a54bfd1_1753993092.jpg
                    - qc_81d9968a-0821-46ff-b0a4-f0865e75f8f1_1753993297.jpg
                    - qc_be38be36-9fe1-413a-8af6-afcb5ee37541_1753991022.jpg
                    - qc_263beec4-357a-4a5f-9009-bde3b387fcb9_1753988800.jpg
                    - qc_e9bc3c0d-d3a1-4c87-87c7-bd077a9ab792_1754057196.jpg
                    - qc_26b1c995-4813-4489-9634-2842ec2bbc71_1753992811.jpg
                    - qc_a9715c64-65fc-4049-b38b-9bb0e259131c_1754154954.jpg
                    - qc_d7c30b32-4d48-4dff-b61e-297010695667_1753993308.jpg
                    - qc_8830864e-2ece-4a4f-8816-5e48b2fbcbb7_1754091973.jpg
                    - qc_2d0cfce8-1438-4a7e-9258-ca78e332b009_1754064407.jpg
                    - qc_29cddfea-f464-4237-b487-73bd36e4bfe7_1753988997.jpg
                    - qc_07be950e-ad16-4c61-82cf-8dedf26a317f_1754064325.jpg
                    - qc_22db2802-ef8d-43a7-9d47-c33c03dfcdbe_1754153406.jpg
                    - qc_268dcd29-9afc-495b-9aa2-5b17888429cc_1753992886.jpg
                    - qc_23949b8e-0da1-421d-8117-2061b7c6e6f9_1753993737.jpg
                    - qc_814ccd27-e236-403a-aff1-382e74cac1e0_1754057105.jpg
                    - qc_1b6a69d1-495a-47e4-9a2f-526d813e9802_1753994015.jpg
                    - qc_ddfccc98-306e-4cb5-8f65-e4561d9b883f_1753993081.jpg
                    - qc_61c3bc97-0a7c-46c0-86cd-6aada9a7ca89_1754153471.jpg
                    - qc_fe935343-26ed-4a86-9cde-095afb7d9753_1754153504.jpg
                    - qc_87e98eed-c4b4-4d53-80c1-55f85e591c00_1753992283.jpg
                    - qc_ebe84e33-5275-4ff6-966c-e53fa3a7e87c_1753993544.jpg
                    - qc_935bde23-c5c6-494c-b40f-1e1dee43bd2f_1754081562.jpg
                    - qc_385f76fd-2e7f-4625-b355-47d0c706828e_1754064355.jpg
                    - qc_c32b7026-2e6c-4022-8dfd-31dff7305a02_1754064372.jpg
                    - qc_8be78fa4-0646-4a6c-be1e-787d7bde5d85_1753988821.jpg
                    - qc_baeab100-6274-4f00-b76a-ec94439a6d23_1753993812.jpg
                    - qc_34689c85-045e-42dd-9fa1-8a4eb4c0ff58_1753992712.jpg
                    - qc_bcadec1b-796d-46b0-99ba-4062a2f739c5_1753991033.jpg
                    - qc_3290a6ae-0710-40ac-a624-29c6ef9dfce6_1754081816.jpg
                    - qc_2d03cb7c-d53a-43a4-a3d2-02005ba0d57a_1753992865.jpg
                    - qc_c323122b-2c51-4b65-95bc-985e0c668540_1754091995.jpg
                    - qc_f48ab9a4-413b-480e-a95a-a8717ea6001e_1754081849.jpg
                    - qc_5b98e138-d36f-4b72-81aa-3dbc07180376_1753993469.jpg
                    - qc_3419a155-bfe2-44f4-8910-ca7068001e1b_1754155446.jpg
                    - qc_75f65cbe-0dfb-42a3-b2b5-7b3108679908_1753993651.jpg
                    - qc_d8bccf99-f840-48df-86bd-35ab4b664559_1754081860.jpg
                    - qc_b18b1696-7be6-4536-96e1-55094bd57e4f_1754088729.jpg
                    - qc_db6beb91-3487-4a63-b2df-a1ea41848097_1754155155.jpg
                    - qc_4a1ba918-9668-42d2-8553-9df96f4c446f_1753988942.jpg
                    - qc_9106831c-c0ed-41cb-9e29-3851000e614e_1753988690.jpg
                    - qc_874ea823-a5c7-4f85-ad3c-26322e066145_1754057140.jpg
                    - qc_7f4765cb-4483-43fc-a3ec-cafa002a0b40_1753992559.jpg
                    - qc_627796ca-3f64-403e-b91f-d8882426fdf8_1753993897.jpg
                    - qc_ffe2f5fb-9a9d-4d35-a297-c0c08537836d_1753992821.jpg
                    - qc_7bba6c64-c821-463b-ad1f-791e52b74b7a_1753992832.jpg
                    - qc_4e9a9315-5029-4555-b076-61f308a295ae_1754091962.jpg
                    - qc_eb38a9d1-b940-43b9-b5b8-19b7a1b10140_1754064356.jpg
                    - qc_44734607-55dc-449c-95b5-70c41a54fcbd_1754064383.jpg
                    - qc_04b00e45-8e0b-415b-8738-9bd6b5f63a60_1753994121.jpg
                    - qc_d2ca9df8-6168-48ee-8968-0651592b5249_1753992021.jpg
                    - qc_e6c451ed-1d47-4046-83cc-e34bffa22488_1754064320.jpg
                    - qc_cb1e5c63-7ed6-42b3-b824-3aeb9caea3ad_1753988734.jpg
                    - qc_bca85d2f-eb79-4775-9e1c-f061270b3146_1753992669.jpg
                    - qc_ac2ac8bd-e332-4aba-a79e-3be45ab40d35_1753993501.jpg
                    - qc_68bccfd4-438b-4a40-adc6-656a27fcaad9_1753994058.jpg
                    - qc_ec610b6a-3eb8-45ce-8971-374937a3104f_1754091928.jpg
                    - qc_f5caeb59-86b3-4550-b0cd-9a7811c72348_1753993523.jpg
                    - qc_ebbcdf44-1662-4952-a789-cbe9396ca609_1754153469.jpg
                    - qc_b1283eeb-68ef-46ba-b4d6-2951c3f8a2f4_1753992941.jpg
                    - qc_cfb1e404-3377-4afe-96ec-4a569d258c1a_1754088740.jpg
                    - qc_a98bd5a3-5188-47be-a5e6-3ba9f5fcfd75_1753988535.jpg
                    - qc_16be20f5-e7f9-48b2-8521-903d8d403bfc_1754074637.jpg
                    - qc_bae43b97-28c6-460e-978d-9c932efd104b_1754071227.jpg
                    - qc_9ad2f8f9-e701-41ab-8091-5aaade2c096b_1754155068.jpg
                    - qc_5f8784d5-8dee-4c07-b681-3459d0f84bef_1753988468.jpg
                    - qc_8e2ac6db-e03d-4466-9f0b-242ef9922dca_1754091212.jpg
                    - qc_fd0efef7-5873-454b-a850-cf33a482894d_1753993662.jpg
                    - qc_40894070-4115-43da-afdc-897e7bae423b_1753993394.jpg
                    - qc_db8a866f-bb9c-4561-a810-ab8276b45a44_1753992636.jpg
                    - qc_39d5ecc1-1d4d-481f-82b4-81e2a5d426ca_1754082798.jpg
                    - qc_5e982366-0241-42ac-a737-bf055d0a069d_1754094129.jpg
                    - qc_e204725c-1534-49cb-8728-3c67fe3b6d4f_1753993587.jpg
                    - qc_3244e165-4a88-4c28-89f6-db6c5d1e2b93_1753988767.jpg
                    - qc_9a6dc151-8add-4f41-ad75-bd83aff5ac7a_1753993684.jpg
                    - qc_a76c0b18-93af-47c8-95e1-e7cc763749a9_1754059743.jpg
                    - qc_a2e8937d-0087-4fa2-84cc-3bd572f901bf_1753993017.jpg
                    - qc_afb2e53a-358d-4af6-acf0-be49723406a0_1753994153.jpg
                    - qc_9a221700-d4b1-4e31-af3a-44d4f18d9602_1754091146.jpg
                    - qc_6eea3043-828e-41aa-8a47-7c77c95300a2_1754064371.jpg
                    - qc_fab7a5f1-d341-4f85-a75b-e844f6fb789b_1754071216.jpg
                    - qc_2d76a948-7d1c-4814-bbc9-2809dcf12c6b_1753992151.jpg
                    - qc_778ae922-9f99-42e1-a3a4-b6f90e980acb_1753993437.jpg
                    - qc_74ed94e7-1f0e-4606-adcd-207672c712a7_1753990500.jpg
                    - qc_974ffa12-ebb7-473a-a2be-4758bf4aca81_1753993758.jpg
                    - qc_f532c5e5-c34f-407d-a7cf-205a44f03e3f_1754155443.jpg
                    - qc_84769586-ac24-4416-96f9-4a027ff247f8_1753988700.jpg
                    - qc_941f93cd-2a5b-4cc3-9943-bd26c9eb0ed5_1753988865.jpg
                    - qc_675bc5a1-30a1-4866-b1f7-1090f6fcb7a2_1753992433.jpg
                    - qc_07e5116e-bcb1-4977-8b9d-d773d4551be9_1753988975.jpg
                    - qc_441b1e72-94b4-48b4-a337-1f027c0b3e38_1753993801.jpg
                    - qc_550816f9-6b61-4f72-942d-67985a7ea476_1753992778.jpg
                    - qc_7046b0c5-2280-46c6-9fe8-c8050db697a4_1754064317.jpg
                    - qc_2d331f0b-96c0-4ed3-9422-c90e88bacf9d_1754057381.jpg
                    - qc_b11f812b-b2c7-4176-b705-a09a5a13c080_1753994036.jpg
                    - qc_aa7c87a4-ed88-48d4-a6dd-66649e33f3b1_1754081630.jpg
                    - qc_2ef70ed8-429a-4f02-981b-20f4952a8d61_1753988645.jpg
                    - qc_923b093b-e834-4fbe-b7ed-d7beb19f7324_1754153396.jpg
                    - qc_01227679-d735-402b-a7a2-8c41749a2fa4_1754070959.jpg
                    - qc_939b2017-d49f-4f11-ad84-c1f279536d3b_1753992272.jpg
                    - qc_4c4e5af2-3d7a-4fd2-af8c-84f8d5b77692_1753988778.jpg
                    - qc_578d6583-91ef-43c3-8f70-21ca9ea3578e_1753992614.jpg
                    - qc_c4c592bd-5d4f-413b-8149-c49f29d9c5c3_1754064314.jpg
                    - qc_d5667756-afa2-422a-a92f-7c0e8ef1a51e_1754057138.jpg
                    - qc_290990b6-c4d4-4976-80c9-319f91817af6_1754155578.jpg
                    - qc_1c0098e1-25f9-4c0e-929e-ae6e94ee3cd7_1753993887.jpg
                    - qc_a01125eb-92ba-4dda-9eb6-c181605a59d4_1753988656.jpg
                    - qc_97bd299a-2600-4c93-9ad3-38bab96c4ce4_1753991075.jpg
                    - qc_8797632a-0e33-4209-88ed-779aed3f0d49_1753988523.jpg
                    - qc_0b55c959-e99c-40d5-ad59-a9be93c15302_1754081905.jpg
                    - qc_8fb47e87-6124-4adf-8918-faf13280bd47_1754155020.jpg
                    - qc_dab1918f-b8e3-4f61-94cb-6a0b990d50b3_1754081742.jpg
                    - qc_0b7496ee-8ce6-4e00-bbaf-41644d899ef2_1753993405.jpg
                    - qc_8832caaf-9d29-4f37-a3b8-64a2c93ccbfb_1754091833.jpg
                    - qc_a47f76a3-e96e-49b9-b879-a64144258d31_1753992526.jpg
                    - qc_94c2443b-cb53-479c-a8cf-563de79a28af_1753993006.jpg
                    - qc_66e5e1b0-5790-49b3-a56b-c3284939250d_1754155071.jpg
                    - qc_753ec6d0-58b4-45ef-a2f8-9352e11714fc_1753993694.jpg
                    - qc_a32483a3-ed35-4f7e-ad05-619d7b63c385_1753992756.jpg
                    - qc_40168a96-e293-4405-a96b-f6c8d8581107_1753993865.jpg
                    - qc_9cfc31d0-cd33-4e9a-bb7e-6284c3152f6a_1753992876.jpg
                    - qc_a8c44b01-bdb8-4aa4-a8f4-8e91de818491_1754092006.jpg
                    - qc_48902c17-a509-4903-81a3-136f09ca0ca4_1754049227.jpg
                    - qc_8e670010-ba65-45d3-b6b6-188f0ecb2efa_1753992691.jpg
                    - qc_b75b0c21-8575-4925-a17c-c9d522c24660_1753994026.jpg
                    - qc_966f08dc-9e3d-4d17-be66-55fad3a157fe_1753993716.jpg
                    - qc_ddbd9014-bcd7-45bf-b587-7742dd3d3f7b_1753994004.jpg
                    - qc_6d95eff0-94f1-46fb-a1a6-2ae0efe72431_1754074749.jpg
                    - qc_a6cc00f6-ce2f-4b6b-b94e-2cc4da62a729_1754064363.jpg
                    - qc_0baabbc8-d137-4dc6-9336-a2e8dce29afd_1754081827.jpg
                    - qc_a1efd1eb-f89d-40de-80a4-2161e49be466_1754059685.jpg
                    - qc_649c22c3-31aa-40e3-8405-f2f66f53c7f3_1754057141.jpg
                    - qc_2daa0344-c576-43f6-882b-618f47c1a4e3_1754091822.jpg
                    - qc_c4a29bb7-6db0-4d6f-9ec6-07d10093cf05_1754153479.jpg
                    - qc_e97d9934-575e-47d2-8f75-f2f2a2c5541c_1753993876.jpg
                    - qc_a05ac993-17ce-497b-bfe6-a74f056976aa_1753992323.jpg
                    - qc_7950a904-1b94-4b4a-af43-57c5764917ea_1753992537.jpg
                    - qc_6659a611-7e2e-4c73-86ae-610852ef3b1a_1754155470.jpg
                    - qc_4b0723b5-5f35-4a2f-9d11-52589ec424b6_1754057381.jpg
                    - qc_9bb2dfe3-25f7-40d7-afb0-8b6378104626_1753988379.jpg
                    - qc_031ea613-f00d-43eb-9a9f-cc2135d0dcd0_1754064357.jpg
                    - qc_5f709372-14cd-4672-857d-f2c607ce967d_1753992455.jpg
                    - qc_dfc05d9f-6887-4efc-ba0b-b5e8f25d793a_1753993114.jpg
                    - qc_e3673ba4-10aa-47ec-b641-b177fb9dc6c1_1753988557.jpg
                    - qc_a808f810-44cf-4edc-b2d0-861607b18e93_1753994068.jpg
                    - qc_7c099290-e770-4772-887f-586c2da085d6_1753988789.jpg
                    - qc_227446b0-2a01-42cb-b14b-c7b76b52cf88_1754074590.jpg
                    - qc_569bf802-0297-4f62-991f-96356b40b34b_1754057107.jpg
                    - qc_d856609b-aa39-4de6-97db-32f7d3734710_1754057384.jpg
                    - qc_ac894a20-8195-455e-8c8b-422d0e5cdd55_1754081764.jpg
                    - qc_d0a53588-f337-4ee8-9779-dedb636012c6_1753993994.jpg
                    - qc_66f18c87-099c-469e-be20-640b0e503c7c_1753993823.jpg
                    - qc_43ecaca5-8a33-47bc-a994-21d23f30552b_1754070941.jpg
                    - qc_970506a8-6d95-43e4-98b9-f7ad74338d47_1753993951.jpg
                    - qc_29072e06-e328-438e-96d9-64ce76eb3107_1753988667.jpg
                    - qc_9cf1538f-97d8-45ae-84d0-af689372f433_1753992356.jpg
                    - qc_2a79c9b0-a39e-4d51-af15-7c90ebe3571c_1754074659.jpg
                    - qc_1e95b6c7-5eca-4931-9f89-c4453de3095f_1754070929.jpg
                    - qc_2335f69a-e543-40b4-9bca-8dadf6631bad_1753988590.jpg
                    - qc_a91d3528-5b33-4e23-9619-15c4d4a4f9ed_1753992919.jpg
                    - qc_22ebb8a6-85dd-40dc-b4f9-b47bf3608d6c_1753992701.jpg
                    - qc_275ba075-ff2f-4041-bacb-24a905c9e603_1753993254.jpg
                    - qc_b40702e6-591a-46e4-922a-5d11aae8cd3f_1754155240.jpg
                    - qc_bb44e60b-144e-454c-90dc-a72421b76ccd_1753988412.jpg
                    - qc_64511971-d59b-41aa-8331-c335fdc31b73_1754153400.jpg
                    - qc_a8b31474-1bed-4155-8733-dd6aa554fe7c_1753993222.jpg
                    - qc_e5e390af-e43c-45b2-b828-80923c2519a1_1753993598.jpg
                    - qc_d7746840-8aad-4dca-b080-3b1fadd3bf0b_1753992930.jpg
                    - qc_565a0fa8-435c-4d9a-aa62-b64aca7f44f3_1753988811.jpg
                    - qc_a9642a48-d0e0-4f3f-ad91-8cb40c497d10_1753993533.jpg
                    - qc_4388aa71-9426-4055-918f-69a6fbdfe051_1753992400.jpg
                    - qc_d0d21727-094a-40cb-8ec8-7c4a7e4d47b3_1754081663.jpg
                    - qc_2583f5e7-ecfb-416c-90b9-c1fa72c2101d_1754091856.jpg
                    - qc_ce2c4bdf-55cd-4038-a450-a25c3786ef23_1753992297.jpg
                    - qc_3955b8ef-6404-4930-9bd8-fbc8448fa2d6_1753993555.jpg
                    - qc_e61e41cd-6f43-4e16-8c7f-afc81b865771_1753993791.jpg
                    - qc_1169e544-6689-479b-b601-7b733891592e_1754153418.jpg
                    - qc_483d6bf5-47f2-43f9-be30-2a8881565206_1753993146.jpg
                    - qc_1c61fadd-38a7-4739-a424-db553cc7394e_1753988424.jpg
                    - qc_db31bd63-7d9f-47ef-bb8c-f0a5569bced2_1753994164.jpg
                    - qc_a0f69825-2aa4-4db9-8337-3619a68fd6f8_1753993286.jpg
                    - qc_f3992344-b0b2-4f35-a3f3-3209621797ec_1753992140.jpg
                    - qc_55c9ec1c-82a5-41f3-b5f5-bec5bf6458c1_1754081585.jpg
                    - qc_5fb6cc28-5835-4f05-8950-9a29b486b9be_1753988723.jpg
                    - qc_a014759a-2044-4b36-b311-8e85df6e3e49_1754064372.jpg
                    - qc_ed7c1438-c8e3-48c7-a607-a860457e842a_1753993844.jpg
                    - qc_3c1bcafb-9a27-4f6c-929b-07f4e688394b_1753993179.jpg
                    - qc_66d69bc7-0c5a-4d79-8f9b-fe7c210ec8ca_1754081705.jpg
                    - qc_e37b262c-7d30-43a2-9755-7fd5895ac69f_1754091811.jpg
                    - qc_81539888-325c-463f-86e5-fa263fe27565_1753993705.jpg
                    - qc_202fe337-5f8b-4e32-88e3-1c4dfdfa2bc0_1753993726.jpg
                    - qc_148cd8f4-10a2-405e-a83d-5c9fbbe1a2c1_1753992345.jpg
                    - qc_880592a6-91f5-4c4d-9893-0c9f0fa9ade7_1754064364.jpg
                    - qc_1cbb6cd7-2291-4bb9-b5c6-fa028888987c_1753988401.jpg
                    - qc_07e80a87-a93f-47d2-b13b-5f3ffb73b9e1_1753993641.jpg
                    - qc_c437ae0f-1d40-4c5d-949d-d95e75f07fd6_1753994100.jpg
                    - qc_a62f7c87-57d0-4f1d-a15b-a2b73a2578ff_1754089065.jpg
                    - qc_9b420372-9315-4ebe-808d-005ef17f8ff6_1754155534.jpg
                    - qc_1dd10219-664c-47f0-b6ca-602b4e327151_1753991086.jpg
                    - qc_57cdf85c-b32b-4432-82d3-2737d8a6d7a8_1753988931.jpg
                    - qc_297ee86a-5d13-40c8-bb02-bc4fec998ff0_1753992129.jpg
                    - qc_d97df5aa-ae71-437d-a867-b8b614b1b83a_1754088947.jpg
                    - qc_b6f844b9-836c-4d09-a1ef-f132903b5178_1753993961.jpg
                    - qc_78e65178-ef13-4c5e-8346-aa7692dbab22_1753988712.jpg
                    - qc_9bf6583b-b6ea-4dbf-9c9e-a2247e8b452d_1753994047.jpg
                    - qc_4daa9635-c41a-4a8a-99e3-cd7e2f69c1cf_1753993372.jpg
                    - qc_c848c2b7-ca85-412e-9178-9c1dd8f11fb1_1753993027.jpg
                    - qc_3f580da1-f7a8-4260-818a-64bc21b32278_1753992995.jpg
                    - qc_7ce73a01-5020-4000-8f89-4cbb6b11a520_1754064446.jpg
                    - qc_b3c96b96-99fc-483d-a6af-89c073682e08_1753988512.jpg
                    - qc_401f1fd3-2a51-47b0-859b-14a73e2e4b60_1753993243.jpg
                    - qc_e42e4f13-163f-4ea2-ab19-3ea584e29eaf_1753994079.jpg
                    - qc_08349232-ed43-44e3-85f0-4891250dfad0_1754059695.jpg
                    - qc_69efef74-1126-4098-a498-e2e429fec0b8_1753994207.jpg
                    - qc_14d0bf72-c8ab-4157-93fa-ed20f9b313ae_1753993491.jpg
                    - qc_e251095c-5a05-4507-a1ff-a0a2f45a7e66_1754081607.jpg
                    - qc_9a3da3aa-7084-4c95-83da-758167743581_1754064364.jpg
                    - qc_df063557-c04e-4951-8416-0733224cf1fc_1753993566.jpg
                    - qc_4386075f-cea8-43ec-be8f-77cc39332e89_1754091168.jpg
                    - qc_65957685-ddc0-49d6-a827-6fa11672ec0c_1754038498.jpg
                    - qc_427a762b-5978-4553-b77d-3e2b4f5c187d_1754088717.jpg
                    - qc_2b3f2374-c111-474e-a258-83dabbef7627_1754094118.jpg
                    - qc_a86acfd3-63c3-42c0-bfa8-0d3a837fb044_1753993200.jpg
                    - qc_e0953843-6ae4-4a52-ad12-33de5d3a488c_1753993458.jpg
                    - qc_d92bac8e-f372-4d04-9635-595791aa2cf4_1754064393.jpg
                    - qc_653f03a0-da48-4b5f-a8cc-2399bcabe203_1753988623.jpg
                    - qc_f1779ad6-91af-4729-939a-11bf06db8cb9_1754064379.jpg
                    - qc_9aa9f3a8-9e03-4f33-b57b-edf1856b0676_1753988490.jpg
                    - qc_b7db9375-ad60-4560-a60f-ffa65e29038d_1754091800.jpg
                    - qc_e77a981f-afd5-4d02-8cfe-b7d4c572ca56_1754089026.jpg
                    - qc_41ece90f-63f4-43d2-a0d6-c29a7f295f9c_1753993265.jpg
                    - qc_7bc00100-ea19-4f0a-9992-85f4c929dcde_1754082814.jpg
                    - qc_7cf35d9e-816c-4d3f-97eb-2157860e8359_1754089048.jpg
                    - qc_ff988d77-d092-428e-a10d-685b06f068a3_1753988876.jpg
                    - qc_c5c1da21-84f2-48ba-b5ca-cdee954c84a7_1753994132.jpg
                    - qc_d1d59b3a-2cc9-4583-82c0-e9c465306106_1754153390.jpg
                    - qc_3a038140-a18a-4b60-9927-c293be7ba681_1754088981.jpg
                    - qc_3c3015ec-8315-4225-ba47-1c4e3665b1e1_1754081302.jpg
                    - qc_ba17c683-4d97-4f26-801d-6ae0716058b4_1754089037.jpg
                    - qc_6f9fb896-b58c-4ed1-b9b1-e3fed190bd58_1753988854.jpg
                    - qc_52323ef9-53ec-4de6-82ea-1dda38a848fd_1753992471.jpg
                    - qc_a6ec9ba7-edd7-4a48-bd9a-6e5979102a75_1754057396.jpg
                    - qc_fe24bbc4-6f5a-480e-ad14-1fb70a6bbc39_1754153501.jpg
                    - qc_130e4dd3-3e20-4a4e-9d92-3acd6334b69b_1753992908.jpg
                    - qc_dc8e1005-4927-44b7-828c-d464ecaaee38_1754091157.jpg
                    - qc_fca2c711-5d5b-4b4f-a4f1-2a349a11cde5_1753989008.jpg
                    - qc_1e926c0e-0470-4d6f-bcf3-65fd75cf3c98_1754049274.jpg
                    - qc_d801ba8f-9944-4933-85b6-12224d437048_1754064310.jpg
            - images/
                - placeholder.jpg
        - templates/
            - index.html
            - gallery_rpi.html
            - status.html
            - live_view.html
            - reports.html
            - operators.html
            - live_view_rpi.html
            - logs.html
            - profiles.html
            - gallery.html
            - connections.html
            - gallery_usb.html
            - live_view_usb.html
            - api.html
            - products.html
            - help.html
            - hardware.html
            - dashboard.html
            - run_history.html
            - base.html
    - config/
        - __init__.py
        - settings.py
        - __pycache__/
            - __init__.cpython-311.pyc
            - settings.cpython-311.pyc
    - services/
        - camera_service_rpi.py
        - camera_service_usb.py
    - tests/
        - test_api.py
        - conftest.py
        - test_models.py
        - test_services.py

# Python Files Content

---

### `main.py`

```python
"""
The main application entry point.

REVISED: All AI-related service initialization and Redis state management
has been removed to create a non-AI version of the application.

DEFINITIVE FIX: The broadcast loop now combines system and orchestration status
into a single message before sending. This prevents client-side JSON parsing
errors caused by receiving multiple messages in a single network packet.
"""
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import redis.asyncio as redis

PROJECT_ROOT = Path(__file__).parent

from config import settings, ACTIVE_CAMERA_IDS
from app.models.database import engine, Base, AsyncSessionFactory
from app.api.v1 import api_router as api_v1_router
from app.web.router import router as web_router
from app.websocket.router import router as websocket_router
from app.middleware.metrics_middleware import MetricsMiddleware

if settings.APP_ENV == "development":
    from app.api.v1 import debug as debug_router

# Import all core services
from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.modbus_poller import AsyncModbusPoller
from app.services.detection_service import AsyncDetectionService
from app.services.system_service import AsyncSystemService
from app.services.notification_service import AsyncNotificationService
from app.services.orchestration_service import AsyncOrchestrationService
from app.websocket.connection_manager import manager as websocket_manager


class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"--- Application starting up in {settings.APP_ENV} mode... ---")

    # Initialize database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables verified.")

    # Initialize Redis client
    app.state.redis_client = redis.from_url("redis://localhost", decode_responses=True)

    # Initialize all application services
    app.state.modbus_controller = await AsyncModbusController.get_instance()
    app.state.orchestration_service = AsyncOrchestrationService(
        modbus_controller=app.state.modbus_controller,
        db_session_factory=AsyncSessionFactory,
        redis_client=app.state.redis_client,
        app_settings=settings
    )
    app.state.notification_service = AsyncNotificationService(db_session_factory=AsyncSessionFactory)
    app.state.camera_manager = AsyncCameraManager(
        notification_service=app.state.notification_service,
        captures_dir=settings.CAMERA_CAPTURES_DIR
    )
    
    # MODIFIED: Pass the db session factory back in, as it's now required
    app.state.detection_service = AsyncDetectionService(
        modbus_controller=app.state.modbus_controller,
        camera_manager=app.state.camera_manager,
        orchestration_service=app.state.orchestration_service,
        conveyor_settings=settings.CONVEYOR,
        db_session_factory=AsyncSessionFactory # This is now correct
    )

    app.state.modbus_poller = AsyncModbusPoller(
        modbus_controller=app.state.modbus_controller,
        event_callback=app.state.detection_service.handle_sensor_event,
        sensor_config=settings.SENSORS
    )
    app.state.system_service = AsyncSystemService(
        modbus_controller=app.state.modbus_controller,
        modbus_poller=app.state.modbus_poller,
        camera_manager=app.state.camera_manager,
        detection_service=app.state.detection_service,
        orchestration_service=app.state.orchestration_service,
        settings=settings
    )

    await app.state.orchestration_service.initialize_hardware_state()
    app.state.active_camera_ids = ACTIVE_CAMERA_IDS

    # Start all background tasks
    app.state.notification_service.start()
    app.state.modbus_poller.start()
    app.state.camera_manager.start()

    # The broadcast loop for sending status updates to the UI
    async def broadcast_updates():
        while True:
            try:
                system_status = await app.state.system_service.get_system_status()
                orchestration_status = app.state.orchestration_service.get_status()

                full_status_payload = {
                    "system": system_status,
                    "orchestration": orchestration_status
                }

                await websocket_manager.broadcast_json({"type": "full_status", "data": full_status_payload})
                
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in broadcast loop: {e}")
                await asyncio.sleep(5)

    app.state.broadcast_task = asyncio.create_task(broadcast_updates())
    await app.state.notification_service.send_alert("INFO", "Application startup complete.")
    print("--- Application startup complete. Server is online. ---")

    yield

    # Graceful shutdown sequence
    print("--- Application shutting down... ---")
    await app.state.redis_client.close()
    if 'broadcast_task' in app.state and app.state.broadcast_task:
        app.state.broadcast_task.cancel()
    await app.state.modbus_poller.stop()
    app.state.notification_service.stop()
    await app.state.camera_manager.stop()
    await app.state.modbus_controller.disconnect()
    await engine.dispose()
    print("--- Application shutdown complete. ---")

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)
    
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    
    app.mount("/static", NoCacheStaticFiles(directory=PROJECT_ROOT / "web/static"), name="static")
    app.mount("/captures", NoCacheStaticFiles(directory=PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR), name="captures")
    
    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(web_router)
    app.include_router(websocket_router)
    
    if settings.APP_ENV == "development":
        app.include_router(debug_router.router, prefix="/api/v1/debug", tags=["Debug"])
        
    app.state.templates = Jinja2Templates(directory=str(PROJECT_ROOT / "web/templates"))
    return app

app = create_app()
```

---

### `app/__init__.py`

```python
# This file is empty.

```

---

### `app/websocket/__init__.py`

```python
# This file is empty.

```

---

### `app/websocket/connection_manager.py`

```python
"""
Manages all active WebSocket connections.
This file is already correct, but provided for completeness.
"""
import asyncio
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts a new websocket connection and adds it to the active list."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a websocket connection from the active list."""
        self.active_connections.remove(websocket)

    async def broadcast_json(self, data: dict):
        """Broadcasts a JSON message to all connected clients concurrently."""
        if not self.active_connections:
            return

        # Create a list of tasks for sending messages
        tasks = [conn.send_json(data) for conn in self.active_connections]
        
        # gather waits for all tasks to complete. return_exceptions=True prevents
        # one failed send from crashing the entire broadcast loop.
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Optional: Log any errors that occurred during broadcast
        for result in results:
            if isinstance(result, Exception):
                print(f"Error broadcasting websocket message: {result}")

# A single, shared instance for the entire application
manager = ConnectionManager()
```

---

### `app/websocket/router.py`

```python
"""
Defines the WebSocket endpoint.
REVISED: The entire connection lifecycle is now wrapped in a single
try/finally block. This is a more robust pattern that guarantees
the disconnect logic is always called, even if an error occurs
immediately after connection. This resolves the handshake error.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .connection_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # The fix is to handle the connection and disconnection in a try/finally block.
    await manager.connect(websocket)
    try:
        # This loop keeps the connection open.
        # It waits for the client to send a message (which we don't use)
        # or for the connection to be closed by the client or server.
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # This block is executed when the client's browser closes the connection.
        print("A client disconnected cleanly.")
    except Exception as e:
        # This can catch other unexpected errors.
        print(f"An unexpected error occurred in the websocket connection: {e}")
    finally:
        # This block is GUARANTEED to run, whether the disconnect was
        # clean or caused by an error. This prevents stale connections.
        manager.disconnect(websocket)
        print("Connection resources cleaned up.")
```

---

### `app/api/v1/__init__.py`

```python
from fastapi import APIRouter

# Import the MODULES where the routers are defined.
from . import system
from . import detection
from . import outputs
from . import camera
from . import profiles
from . import orchestration
from . import products
from . import operators
from . import run_history
# This line is correct from the traceback
from . import reports

# Create the main router for the v1 API.
api_router = APIRouter()

# Include the `router` OBJECT from each of the imported modules.
api_router.include_router(system.router, prefix="/system", tags=["System & Monitoring"])
api_router.include_router(detection.router, prefix="/detection", tags=["Box Detection"])
api_router.include_router(outputs.router, prefix="/outputs", tags=["Hardware Control"])
api_router.include_router(camera.router, prefix="/camera", tags=["Camera"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profile Management"])
api_router.include_router(orchestration.router, prefix="/orchestration", tags=["Run Orchestration"])
api_router.include_router(products.router, prefix="/products", tags=["Product Master"])
api_router.include_router(operators.router, prefix="/operators", tags=["Operator Master"])
api_router.include_router(run_history.router, prefix="/run-history", tags=["Run History"])

# THIS IS THE FIX: The router from the 'reports' module must be included.
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
```

---

### `app/api/v1/operators.py`

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import get_async_session, Operator
from app.schemas.operators import OperatorCreate, OperatorUpdate, OperatorOut

router = APIRouter()

@router.post("/", status_code=201, response_model=OperatorOut)
async def create_operator(
    operator_in: OperatorCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new operator."""
    result = await db.execute(select(Operator).where(Operator.name == operator_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"An operator with name '{operator_in.name}' already exists.")
    
    new_operator = Operator(**operator_in.model_dump())
    db.add(new_operator)
    await db.commit()
    await db.refresh(new_operator)
    return new_operator

@router.get("/", response_model=List[OperatorOut])
async def get_all_operators(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all operators."""
    result = await db.execute(select(Operator).order_by(Operator.name))
    return result.scalars().all()

@router.get("/{operator_id}", response_model=OperatorOut)
async def get_operator(operator_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single operator by ID."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator

@router.put("/{operator_id}", response_model=OperatorOut)
async def update_operator(
    operator_id: int,
    operator_in: OperatorUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing operator."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    
    update_data = operator_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(operator, key, value)
        
    await db.commit()
    await db.refresh(operator)
    return operator

@router.delete("/{operator_id}", status_code=204)
async def delete_operator(operator_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete an operator."""
    operator = await db.get(Operator, operator_id)
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
        
    await db.delete(operator)
    await db.commit()
    return None
```

---

### `app/api/v1/reports.py`

```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

# --- THIS IS THE FIX ---
# The import is changed from the incorrect 'DetectionEvent' to the correct 'DetectionEventLog'.
from app.models import get_async_session, RunLog, RunStatus, DetectionEventLog
# ---------------------

router = APIRouter()

@router.get("/summary")
async def get_production_summary(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None, description="Start date for the report query (ISO 8601)"),
    end_date: Optional[datetime] = Query(None, description="End date for the report query (ISO 8601)"),
):
    """
    Generates a high-level production summary report for a given date range.
    This calculates total runs, their statuses, and the total number of items detected.
    """
    # Base query to select RunLogs. We use selectinload to efficiently fetch
    # all related detection events in a single follow-up query, preventing the N+1 problem.
    query = select(RunLog).options(selectinload(RunLog.detection_events))

    # Apply date filters if provided
    if start_date:
        query = query.where(RunLog.start_timestamp >= start_date)
    if end_date:
        query = query.where(RunLog.start_timestamp <= end_date)

    result = await db.execute(query)
    runs = result.scalars().all()

    # Calculate statistics from the fetched runs
    total_runs = len(runs)
    total_detections = sum(len(run.detection_events) for run in runs)
    completed_runs = sum(1 for run in runs if run.status == RunStatus.COMPLETED)
    failed_runs = sum(1 for run in runs if run.status == RunStatus.FAILED)
    aborted_runs = sum(1 for run in runs if run.status == RunStatus.ABORTED)

    # Return a structured summary response
    return {
        "query_parameters": {
            "start_date": start_date.isoformat() if start_date else "Not specified",
            "end_date": end_date.isoformat() if end_date else "Not specified",
        },
        "summary": {
            "total_runs_in_period": total_runs,
            "completed_runs": completed_runs,
            "failed_runs": failed_runs,
            "aborted_runs": aborted_runs,
            "total_items_detected": total_detections,
        }
    }
```

---

### `app/api/v1/system.py`

```python
"""
This API router handles high-level system endpoints, including status checks,
version info, emergency stops, and the full system reset.

DEFINITIVE FIX: Removed all obsolete AI-related endpoints (/ai/source, /ai/toggle)
and their associated Pydantic models and dependencies.
"""
from fastapi import APIRouter, Depends, Request
from app.services.system_service import AsyncSystemService
# --- THIS IS THE FIX ---
# The import path is corrected to match your project's directory structure.
from app.api.v1.auth.dependencies import get_api_key, rate_limiter
# -----------------------
from config import settings # Import settings for version

router = APIRouter()

def get_system_service(request: Request) -> AsyncSystemService:
    return request.app.state.system_service

@router.get("/version")
async def get_version():
    """Returns the current running code version to verify updates."""
    return {"version": settings.PROJECT_VERSION}

@router.get("/status", dependencies=[Depends(rate_limiter)])
async def get_system_status(service: AsyncSystemService = Depends(get_system_service)):
    """Get overall system health status."""
    return await service.get_system_status()

@router.post("/reset-all", status_code=200)
async def reset_all_state(service: AsyncSystemService = Depends(get_system_service)):
    """Resets all counters and stops all hardware. A full system state reset."""
    await service.full_system_reset()
    return {"message": "System state has been fully reset."}

@router.post("/emergency-stop", status_code=200, dependencies=[Depends(get_api_key)])
async def emergency_stop(service: AsyncSystemService = Depends(get_system_service)):
    """Immediately stop all hardware operations. Requires API Key."""
    await service.emergency_stop()
    return {"message": "Emergency stop sequence initiated."}
```

---

### `app/api/v1/camera.py`

```python
# rpi_counter_fastapi-dev2/app/api/v1/camera.py

import os
import io
import zipfile
from datetime import datetime as dt_datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query, HTTPException, Path, Body
from fastapi.responses import StreamingResponse
import asyncio
import redis.asyncio as redis
from pydantic import BaseModel
import json

from app.core.camera_manager import AsyncCameraManager
# --- THIS IS THE FIX ---
# We import both `settings` and the `ACTIVE_CAMERA_IDS` list directly from the config package.
from config import settings, ACTIVE_CAMERA_IDS
# --- END OF FIX ---
from pathlib import Path


router = APIRouter()

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

def get_camera_manager(request: Request) -> AsyncCameraManager:
    return request.app.state.camera_manager

def get_redis_client(request: Request) -> redis.Redis:
    return request.app.state.redis_client

class CameraPreviewSettings(BaseModel):
    exposure: Optional[int] = None
    gain: Optional[int] = None
    white_balance_temp: Optional[int] = None
    brightness: Optional[int] = None
    autofocus: Optional[bool] = None

@router.get("/status/{camera_id}")
async def get_camera_status(
    camera_id: str,
    camera: AsyncCameraManager = Depends(get_camera_manager)
):
    status = camera.get_health_status(camera_id)
    return {"camera_id": camera_id, "status": status.value}

@router.get("/stream/{camera_id}")
async def get_camera_stream(camera_id: str, camera: AsyncCameraManager = Depends(get_camera_manager)):
    async def frame_generator():
        frame_queue = await camera.start_stream(camera_id)
        if not frame_queue: return
        try:
            while True:
                frame_bytes = await frame_queue.get()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        finally:
            await camera.stop_stream(camera_id, frame_queue)
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.post("/preview_settings/{camera_id}", status_code=202)
async def apply_preview_settings(
    camera_id: str,
    settings_payload: CameraPreviewSettings,
    redis_client: redis.Redis = Depends(get_redis_client)
):
    # The check now correctly uses the imported `ACTIVE_CAMERA_IDS` list.
    if camera_id not in ACTIVE_CAMERA_IDS:
        raise HTTPException(status_code=404, detail=f"Camera '{camera_id}' is not active or does not exist.")

    command = {
        "action": "apply_settings",
        "settings": settings_payload.model_dump(exclude_none=True)
    }
    channel = f"camera:commands:{camera_id}"
    await redis_client.publish(channel, json.dumps(command))
    return {"message": f"Preview settings applied to camera '{camera_id}'.", "settings": command["settings"]}

@router.get("/captures/{camera_id}")
async def get_captured_images(camera_id: str, page: int = Query(1, ge=1), page_size: int = Query(8, ge=1, le=100)):
    captures_dir = Path(settings.CAMERA_CAPTURES_DIR) / camera_id
    if not captures_dir.exists(): return {"images": [], "has_more": False}
    try:
        image_files = sorted([p for p in captures_dir.glob("*.jpg")], key=lambda p: p.stat().st_mtime, reverse=True)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_files = image_files[start_index:end_index]
        has_more = len(image_files) > end_index
        web_paths = [f"/captures/{camera_id}/{p.name}" for p in paginated_files]
        return {"images": web_paths, "has_more": has_more}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ZipRequestPayload(BaseModel):
    camera_id: str
    start_date: date
    end_date: date

def create_zip_in_memory_sync(camera_id: str, start_date: date, end_date: date) -> io.BytesIO:
    captures_dir = PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR / camera_id
    if not captures_dir.is_dir(): return None
    start_ts = dt_datetime.combine(start_date, dt_datetime.min.time()).timestamp()
    end_ts = dt_datetime.combine(end_date, dt_datetime.max.time()).timestamp()
    files_to_zip = [f for f in captures_dir.glob("*.jpg") if start_ts <= f.stat().st_mtime <= end_ts]
    zip_buffer = io.BytesIO()
    if not files_to_zip: return zip_buffer
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            zipf.write(file_path, arcname=file_path.name)
    zip_buffer.seek(0)
    return zip_buffer

@router.post("/captures/download-zip")
async def download_captures_as_zip(payload: ZipRequestPayload = Body(...)):
    zip_buffer = await asyncio.to_thread(
        create_zip_in_memory_sync, payload.camera_id, payload.start_date, payload.end_date
    )
    if zip_buffer is None: raise HTTPException(status_code=404, detail=f"Capture directory for camera '{payload.camera_id}' not found.")
    if not zip_buffer.getbuffer().nbytes > 0: raise HTTPException(status_code=404, detail="No images found in the specified date range.")
    return StreamingResponse(
        zip_buffer, media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=captures_{payload.camera_id}_{payload.start_date}_to_{payload.end_date}.zip"}
    )

@router.get("/ai_stream/{camera_id}")
async def get_ai_stream(camera_id: str, redis_client: redis.Redis = Depends(get_redis_client)):
    async def ai_frame_generator():
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"ai_stream:frames:{camera_id}")
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=10.0)
                if message and message.get("type") == "message":
                    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + message['data'] + b'\r\n')
        finally:
            await pubsub.close()
    return StreamingResponse(ai_frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")
```

---

### `app/api/v1/profiles.py`

```python
"""
NEW: API endpoints for managing Camera and Object profiles.

This provides the full CRUD (Create, Read, Update, Delete) functionality
required for a UI to manage production "recipes" dynamically without
restarting the application.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import get_async_session, CameraProfile, ObjectProfile, Product
from app.schemas.profiles import (
    CameraProfileCreate, CameraProfileUpdate, CameraProfileOut,
    ObjectProfileCreate, ObjectProfileUpdate, ObjectProfileOut
)

router = APIRouter()

# --- Camera Profile Endpoints ---

@router.post("/camera", status_code=201, response_model=CameraProfileOut)
async def create_camera_profile(
    profile_in: CameraProfileCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new camera profile."""
    # Check if a profile with the same name already exists
    result = await db.execute(select(CameraProfile).where(CameraProfile.name == profile_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"A camera profile with the name '{profile_in.name}' already exists."
        )
    
    new_profile = CameraProfile(**profile_in.model_dump())
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile

@router.get("/camera", response_model=List[CameraProfileOut])
async def get_all_camera_profiles(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all camera profiles."""
    result = await db.execute(select(CameraProfile).order_by(CameraProfile.name))
    return result.scalars().all()

@router.get("/camera/{profile_id}", response_model=CameraProfileOut)
async def get_camera_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single camera profile by its ID."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    return profile

@router.put("/camera/{profile_id}", response_model=CameraProfileOut)
async def update_camera_profile(
    profile_id: int,
    profile_in: CameraProfileUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing camera profile."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    
    update_data = profile_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
        
    await db.commit()
    await db.refresh(profile)
    return profile

@router.delete("/camera/{profile_id}", status_code=204)
async def delete_camera_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete a camera profile."""
    profile = await db.get(CameraProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Camera profile not found")
    
    # Check if any ObjectProfile is using this CameraProfile
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.camera_profile_id == profile_id))
    if result.scalars().first():
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this camera profile. It is currently in use by one or more object profiles."
        )

    await db.delete(profile)
    await db.commit()
    return None

# --- Object Profile Endpoints ---

@router.post("/object", status_code=201, response_model=ObjectProfileOut)
async def create_object_profile(
    profile_in: ObjectProfileCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new object profile."""
    # Check if an object profile with the same name already exists
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.name == profile_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"An object profile with the name '{profile_in.name}' already exists."
        )
    
    # --- PHASE 1: Validate that the product_id exists if provided ---
    if profile_in.product_id:
        product = await db.get(Product, profile_in.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {profile_in.product_id} not found.")

    new_profile = ObjectProfile(**profile_in.model_dump())
    db.add(new_profile)
    await db.commit()
    # We need to load the relationships to return them in the response
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == new_profile.id)
    )
    return result.scalar_one()


@router.get("/object", response_model=List[ObjectProfileOut])
async def get_all_object_profiles(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all object profiles, including their linked camera and product profiles."""
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .order_by(ObjectProfile.name)
    )
    return result.scalars().all()

@router.get("/object/{profile_id}", response_model=ObjectProfileOut)
async def get_object_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single object profile by ID."""
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
    return profile

@router.put("/object/{profile_id}", response_model=ObjectProfileOut)
async def update_object_profile(
    profile_id: int,
    profile_in: ObjectProfileUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing object profile."""
    # Use selectinload to fetch the profile and its related camera_profile in one go
    result = await db.execute(
        select(ObjectProfile)
        .options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
        .where(ObjectProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
        
    update_data = profile_in.model_dump(exclude_unset=True)

    # --- PHASE 1: Validate that the product_id exists if provided ---
    if "product_id" in update_data and update_data["product_id"]:
         product = await db.get(Product, update_data["product_id"])
         if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {update_data['product_id']} not found.")

    for key, value in update_data.items():
        setattr(profile, key, value)
        
    await db.commit()
    # Refresh to ensure all data, including relationships, is up to date
    await db.refresh(profile, attribute_names=['product']) # Eagerly refresh the product relationship
    await db.refresh(profile)
    return profile

@router.delete("/object/{profile_id}", status_code=204)
async def delete_object_profile(profile_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete an object profile."""
    profile = await db.get(ObjectProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Object profile not found")
        
    await db.delete(profile)
    await db.commit()
    return None
```

---

### `app/api/v1/products.py`

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import get_async_session, Product, ObjectProfile
from app.schemas.products import ProductCreate, ProductUpdate, ProductOut

router = APIRouter()

@router.post("/", status_code=201, response_model=ProductOut)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Create a new product."""
    result = await db.execute(select(Product).where(Product.name == product_in.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"A product with name '{product_in.name}' already exists.")
    
    new_product = Product(**product_in.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductOut])
async def get_all_products(db: AsyncSession = Depends(get_async_session)):
    """Retrieve all products."""
    result = await db.execute(select(Product).order_by(Product.name))
    return result.scalars().all()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    """Retrieve a single product by its ID."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Update an existing product."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
        
    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    """Delete a product."""
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    result = await db.execute(select(ObjectProfile).where(ObjectProfile.product_id == product_id))
    if result.scalars().first():
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this product. It is currently in use by one or more object profiles."
        )
        
    await db.delete(product)
    await db.commit()
    return None
```

---

### `app/api/v1/outputs.py`

```python
"""
NEW: API endpoints for manually controlling hardware outputs via Modbus.
This replaces the old GPIO control API, preserving the manual toggle feature.
"""
from fastapi import APIRouter, Depends, Request, HTTPException, Path
from typing import Literal

from app.core.modbus_controller import AsyncModbusController

# This is the router for THIS FILE ONLY. It is self-contained.
# It does not know about any other router.
router = APIRouter()

def get_modbus_controller(request: Request) -> AsyncModbusController:
    return request.app.state.modbus_controller

# Define the literal types for valid output names from settings
OutputPinName = Literal["conveyor", "gate", "diverter", "led_green", "led_red", "buzzer", "camera_light"]

@router.post("/toggle/{name}", status_code=200)
async def toggle_output_by_name(
    name: OutputPinName = Path(...),
    io: AsyncModbusController = Depends(get_modbus_controller)
):
    """
    Toggles the state of any configured output coil (Relay, LED, Buzzer).
    Returns the new state ('ON' or 'OFF').
    """
    # When using Path with a Literal, FastAPI passes the string value directly.
    output_name_str = name

    address = io.get_output_address(output_name_str)
    if address is None:
        raise HTTPException(status_code=404, detail=f"Output name '{output_name_str}' not found in configuration.")

    all_coils = await io.read_coils()
    if all_coils is None:
        raise HTTPException(status_code=503, detail="Could not read current coil states from Modbus device.")

    if address >= len(all_coils):
         raise HTTPException(status_code=500, detail=f"Address {address} for '{output_name_str}' is out of bounds for the reported coils.")

    current_state = all_coils[address]
    new_state = not current_state

    success = await io.write_coil(address, new_state)
    if not success:
        raise HTTPException(status_code=503, detail="Failed to write new coil state to Modbus device.")

    return {"output": output_name_str, "new_state": "ON" if new_state else "OFF"}
```

---

### `app/api/v1/debug.py`

```python
"""
Debug endpoints for testing purposes.
This router should only be mounted in a 'development' environment.
"""
from fastapi import APIRouter, Depends, Request, HTTPException, Body
from app.services.detection_service import AsyncDetectionService
from app.core.sensor_events import SensorEvent, SensorState

router = APIRouter()

def get_detection_service(request: Request) -> AsyncDetectionService:
    return request.app.state.detection_service

@router.post("/sensor-event")
async def trigger_sensor_event(
    service: AsyncDetectionService = Depends(get_detection_service),
    sensor_id: int = Body(..., embed=True),
    new_state: SensorState = Body(..., embed=True)
):
    """
    Manually triggers a sensor event to test the detection state machine.
    This provides a 'backdoor' for end-to-end testing without physical hardware.
    
    Example Body:
    {
        "sensor_id": 1,
        "new_state": "triggered"
    }
    """
    print(f"DEBUG: Manually triggering event: Sensor {sensor_id} -> {new_state.name}")
    event = SensorEvent(sensor_id=sensor_id, new_state=new_state)
    await service.handle_sensor_event(event)
    return {"message": "Debug sensor event triggered successfully.", "new_state": service._state.name}

```

---

### `app/api/v1/detection.py`

```python
from fastapi import APIRouter, Depends, Request, HTTPException
from app.services.orchestration_service import AsyncOrchestrationService # MODIFIED
from app.services.detection_service import AsyncDetectionService

router = APIRouter()

# MODIFIED: Dependency changed to OrchestrationService
def get_orchestration_service(request: Request) -> AsyncOrchestrationService:
    return request.app.state.orchestration_service
    
def get_detection_service(request: Request) -> AsyncDetectionService:
    return request.app.state.detection_service

@router.get("/")
async def get_detection_status(service: AsyncOrchestrationService = Depends(get_orchestration_service)): # MODIFIED
    """Get current detection status and counts."""
    # MODIFIED: Get status from the correct service
    status = service.get_status()
    return {
        "counts": {
            "processed": status["run_progress"],
            "target": status["target_count"]
        },
        "state": status["mode"]
    }

@router.post("/reset", status_code=200)
async def reset_counter(service: AsyncDetectionService = Depends(get_detection_service)):
    """Reset the box counter to zero."""
    # This part of the original code had an error. There is no `reset_counter`
    # on the detection service. We will call the orchestration service stop method
    # which performs a full reset of the counts.
    orchestration_service = get_orchestration_service(service._orchestration)
    await orchestration_service.stop_run()
    return {"message": "Counter and run state reset successfully."}
```

---

### `app/api/v1/run_history.py`

```python
import io
import zipfile
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, Path as FastApiPath
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import get_async_session, RunLog, DetectionEventLog
from app.schemas.run_log import RunLogOut, DetectionEventLogOut
from config import settings

router = APIRouter()

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

@router.get("/", response_model=List[RunLogOut])
async def get_run_history(
    db: AsyncSession = Depends(get_async_session),
    start_date: Optional[datetime] = Query(None, description="ISO 8601 format: YYYY-MM-DDTHH:MM:SS"),
    end_date: Optional[datetime] = Query(None, description="ISO 8601 format: YYYY-MM-DDTHH:MM:SS"),
    operator_id: Optional[int] = Query(None),
    product_id: Optional[int] = Query(None),
    batch_code: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Retrieve historical run logs with filtering and pagination.
    """
    query = (
        select(RunLog)
        .options(selectinload(RunLog.operator), selectinload(RunLog.product))
        .order_by(RunLog.start_timestamp.desc())
    )

    if start_date:
        query = query.where(RunLog.start_timestamp >= start_date)
    if end_date:
        query = query.where(RunLog.start_timestamp <= end_date)
    if operator_id:
        query = query.where(RunLog.operator_id == operator_id)
    if product_id:
        query = query.where(RunLog.product_id == product_id)
    if batch_code:
        query = query.where(RunLog.batch_code.ilike(f"%{batch_code}%"))

    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{run_id}/detections", response_model=List[DetectionEventLogOut])
async def get_run_detection_events(
    run_id: int = FastApiPath(..., description="The ID of the run log"),
    db: AsyncSession = Depends(get_async_session)
):
    """Retrieve all detection events (including image paths) for a single run."""
    result = await db.execute(
        select(DetectionEventLog)
        .where(DetectionEventLog.run_log_id == run_id)
        .order_by(DetectionEventLog.timestamp.asc())
    )
    return result.scalars().all()

def create_zip_from_paths_sync(image_web_paths: List[str]) -> io.BytesIO:
    """Synchronously creates a ZIP archive from a list of web paths."""
    captures_base_dir = PROJECT_ROOT / settings.CAMERA_CAPTURES_DIR
    
    files_to_zip = []
    for web_path in image_web_paths:
        if not web_path: continue
        relative_path = web_path.lstrip('/').lstrip('captures').lstrip('/')
        full_path = captures_base_dir / relative_path
        if full_path.exists():
            files_to_zip.append(full_path)

    zip_buffer = io.BytesIO()
    if not files_to_zip:
        return zip_buffer

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            zipf.write(file_path, arcname=file_path.name)
    
    zip_buffer.seek(0)
    return zip_buffer

@router.get("/{run_id}/download-images")
async def download_run_images_zip(
    run_id: int = FastApiPath(..., description="The ID of the run log to download images from"),
    db: AsyncSession = Depends(get_async_session)
):
    """Downloads all captured images for a specific run as a single ZIP file."""
    run_log = await db.get(RunLog, run_id)
    if not run_log:
        raise HTTPException(status_code=404, detail="Run not found.")

    result = await db.execute(
        select(DetectionEventLog.image_path)
        .where(DetectionEventLog.run_log_id == run_id)
    )
    image_paths = result.scalars().all()

    if not any(image_paths):
        raise HTTPException(status_code=404, detail="No images were logged for this run.")

    zip_buffer = await asyncio.to_thread(create_zip_from_paths_sync, image_paths)
    
    if not zip_buffer.getbuffer().nbytes > 0:
         raise HTTPException(status_code=404, detail="Images for this run were logged, but the files could not be found on disk.")

    filename = f"run_{run_id}_{run_log.batch_code}_images.zip"
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```

---

### `app/api/v1/orchestration.py`

```python
"""
REVISED FOR PHASE 3: API endpoints for controlling the high-level
orchestration of production runs. Replaces the old "batch" system.
ADDED: Target count for production runs.
ADDED: Post-batch delay for pausing between runs.
REVISED: The /run/start endpoint is now the single atomic entry point for starting a new run.
PHASE 3: Payload updated to include batch_code and operator_id.
PHASE 4: Added endpoint to acknowledge alarms.
"""
from fastapi import APIRouter, Depends, Request, Body, HTTPException
from pydantic import BaseModel, Field

from app.services.orchestration_service import AsyncOrchestrationService

router = APIRouter()

def get_orchestration_service(request: Request) -> AsyncOrchestrationService:
    """Dependency to get the orchestration service instance."""
    return request.app.state.orchestration_service

class StartRunPayload(BaseModel):
    """Defines the request body for starting a run."""
    object_profile_id: int = Field(..., gt=0, description="The ID of the ObjectProfile to activate for the run.")
    target_count: int = Field(0, ge=0, description="The target number of items for this run. 0 means unlimited.")
    post_batch_delay_sec: int = Field(5, ge=0, description="The time in seconds to pause after the run completes.")
    batch_code: str = Field(..., min_length=1, description="The unique code for this production batch.")
    operator_id: int = Field(..., gt=0, description="The ID of the operator running the batch.")


@router.post("/run/start", status_code=202)
async def start_production_run(
    payload: StartRunPayload,
    service: AsyncOrchestrationService = Depends(get_orchestration_service)
):
    """
    Atomically loads the specified profile, logs the run, configures the camera, and starts the run.
    This is the single endpoint for initiating a production run.
    """
    success = await service.start_run(
        profile_id=payload.object_profile_id,
        target_count=payload.target_count,
        post_batch_delay_sec=payload.post_batch_delay_sec,
        batch_code=payload.batch_code,
        operator_id=payload.operator_id
    )
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to start run. ObjectProfile with ID {payload.object_profile_id} may not exist, the operator ID may be invalid, or the system is in an invalid state to start."
        )
    return {"message": "Production run started successfully."}

@router.post("/run/stop", status_code=202)
async def stop_production_run(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Stops the conveyor belt and unloads the active profile."""
    await service.stop_run()
    return {"message": "Production run stopped and profile unloaded."}

@router.get("/run/status")
async def get_run_status(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Gets the current status of the orchestration service."""
    return service.get_status()

# --- PHASE 4: New endpoint to acknowledge alarms ---
@router.post("/run/acknowledge-alarm", status_code=200)
async def acknowledge_run_alarm(service: AsyncOrchestrationService = Depends(get_orchestration_service)):
    """Acknowledges and clears the current active alarm."""
    await service.acknowledge_alarm()
    return {"message": "Alarm acknowledged successfully."}
```

---

### `app/api/v1/auth/__init__.py`

```python
# This file is empty.

```

---

### `app/api/v1/auth/security.py`

```python
"""
Security-related utility functions, such as password hashing.
"""
from passlib.context import CryptContext

# Use bcrypt for password hashing, a standard and secure choice.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

```

---

### `app/api/v1/auth/dependencies.py`

```python
"""
FastAPI dependencies for handling security aspects like API key auth and rate limiting.
"""
import time
from typing import Dict, List
from fastapi import Request, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings

# --- API Key Authentication ---
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(API_KEY_HEADER)):
    """
    Dependency that verifies the X-API-Key header against the configured API_KEY.
    """
    if api_key == settings.SECURITY.API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

# --- Simple In-Memory Rate Limiting ---
rate_limit_db: Dict[str, List[float]] = {}
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_TIMEFRAME = 60

async def rate_limiter(request: Request):
    """
    Dependency that provides simple IP-based rate limiting.
    """
    client_ip = request.client.host
    current_time = time.monotonic()

    if client_ip not in rate_limit_db:
        rate_limit_db[client_ip] = []

    rate_limit_db[client_ip] = [
        t for t in rate_limit_db[client_ip] if t > current_time - RATE_LIMIT_TIMEFRAME
    ]

    if len(rate_limit_db[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests. Limit is {RATE_LIMIT_REQUESTS} per {RATE_LIMIT_TIMEFRAME} seconds.",
        )
    
    rate_limit_db[client_ip].append(current_time)
```

---

### `app/api/v1/auth/jwt_handler.py`

```python
"""
Functions for creating, encoding, and decoding JSON Web Tokens (JWTs).
"""
import time
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from config import settings

SECRET_KEY = settings.SECURITY.JWT_SECRET_KEY
ALGORITHM = settings.SECURITY.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decodes a JWT access token, returning the payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # This could be due to an expired signature or invalid token
        return None

```

---

### `app/middleware/metrics_middleware.py`

```python
"""
FastAPI middleware to calculate and report request processing time.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.monotonic()
        response = await call_next(request)
        process_time = time.monotonic() - start_time
        response.headers["X-Process-Time-Seconds"] = str(process_time)
        print(f"Request {request.method} {request.url.path} processed in {process_time:.4f} seconds")
        return response

```

---

### `app/core/__init__.py`

```python
# This file is empty.

```

---

### `app/core/modbus_poller.py`

```python
"""
REVISED: Now acts as the Modbus Poller Service.
- It continuously polls BOTH the input and output modules.
- It maintains a complete, up-to-date state of all hardware I/O.
- It detects changes in inputs and fires sensor events.
- It correctly inverts the NPN sensor signal (LOW signal = TRIGGERED).

DEFINITIVE FIX: The poller now uses the injected sensor configuration to determine
which physical channels to monitor, instead of hardcoding a 1-to-1 mapping. This
makes the SENSORS_ENTRY_CHANNEL and SENSORS_EXIT_CHANNEL settings work correctly.
"""
import asyncio
from typing import Callable, Coroutine, Optional, List
from .modbus_controller import AsyncModbusController, ModbusHealthStatus
from .sensor_events import SensorState, SensorEvent
from config import settings

AsyncEventCallback = Callable[[SensorEvent], Coroutine[None, None, None]]

class AsyncModbusPoller:
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        event_callback: AsyncEventCallback,
        sensor_config  # <-- ADDED: Inject the sensor settings object
    ):
        self.modbus_controller = modbus_controller
        self.event_callback = event_callback
        # --- ADDED: Store the sensor configuration ---
        self._sensor_config = sensor_config
        self.polling_interval_sec = settings.MODBUS.POLLING_MS / 1000.0
        self._monitoring_task: Optional[asyncio.Task] = None
        self._verbose = settings.LOGGING.VERBOSE_LOGGING

        # Initialize all states to True (cleared for NPN sensors)
        self._input_channels: List[bool] = [True] * 4
        self._output_channels: List[bool] = [False] * 8
        self._last_known_entry_state: bool = True
        self._last_known_exit_state: bool = True
        self._health_status: ModbusHealthStatus = ModbusHealthStatus.DISCONNECTED

    def get_io_health(self) -> ModbusHealthStatus:
        return self._health_status

    def get_current_input_states(self) -> List[bool]:
        return self._input_channels

    def get_current_output_states(self) -> List[bool]:
        return self._output_channels

    def start(self):
        if self._monitoring_task and not self._monitoring_task.done():
            return
        print(f"Modbus Poller: Starting polling every {self.polling_interval_sec * 1000}ms.")
        print(f"   -> Monitoring Entry Sensor on Channel: {self._sensor_config.ENTRY_CHANNEL}")
        print(f"   -> Monitoring Exit Sensor on Channel:  {self._sensor_config.EXIT_CHANNEL}")
        self._monitoring_task = asyncio.create_task(self._poll_hardware())

    async def stop(self):
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass

    async def _poll_hardware(self):
        while True:
            raw_inputs = await self.modbus_controller.read_digital_inputs()
            raw_outputs = await self.modbus_controller.read_coils()

            if raw_inputs is not None:
                if self._health_status != ModbusHealthStatus.OK:
                    print("Modbus Poller: Re-established connection to IO modules.")
                self._health_status = ModbusHealthStatus.OK
                self._input_channels = raw_inputs
                
                # Update output channels if read was successful
                if raw_outputs is not None:
                    self._output_channels = raw_outputs

                # --- THE REWRITTEN LOGIC ---
                # Convert 1-based config channels to 0-based list indices
                entry_idx = self._sensor_config.ENTRY_CHANNEL - 1
                exit_idx = self._sensor_config.EXIT_CHANNEL - 1

                # Check Entry Sensor state if index is valid
                if 0 <= entry_idx < len(self._input_channels):
                    current_entry_state = self._input_channels[entry_idx]
                    if current_entry_state != self._last_known_entry_state:
                        is_triggered = not current_entry_state  # NPN Logic Inversion
                        if self._verbose:
                            print(f"[Sensor Event] Entry Sensor (Channel {entry_idx + 1}): Raw={current_entry_state} -> {'TRIGGERED' if is_triggered else 'CLEARED'}")
                        event = SensorEvent(
                            sensor_id=self._sensor_config.ENTRY_CHANNEL,
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))
                        self._last_known_entry_state = current_entry_state

                # Check Exit Sensor state if index is valid
                if 0 <= exit_idx < len(self._input_channels):
                    current_exit_state = self._input_channels[exit_idx]
                    if current_exit_state != self._last_known_exit_state:
                        is_triggered = not current_exit_state  # NPN Logic Inversion
                        if self._verbose:
                            print(f"[Sensor Event] Exit Sensor (Channel {exit_idx + 1}): Raw={current_exit_state} -> {'TRIGGERED' if is_triggered else 'CLEARED'}")
                        event = SensorEvent(
                            sensor_id=self._sensor_config.EXIT_CHANNEL,
                            new_state=SensorState.TRIGGERED if is_triggered else SensorState.CLEARED
                        )
                        asyncio.create_task(self.event_callback(event))
                        self._last_known_exit_state = current_exit_state
                # --- END OF REWRITTEN LOGIC ---
                
            else:
                if self._health_status == ModbusHealthStatus.OK:
                    print("Modbus Poller: Lost connection to IO modules.")
                self._health_status = self.modbus_controller.health_status
                
                # If connection is lost, force sensors to a 'cleared' state
                if not self._last_known_entry_state:
                    self._last_known_entry_state = True
                    event = SensorEvent(sensor_id=self._sensor_config.ENTRY_CHANNEL, new_state=SensorState.CLEARED)
                    asyncio.create_task(self.event_callback(event))

                if not self._last_known_exit_state:
                    self._last_known_exit_state = True
                    event = SensorEvent(sensor_id=self._sensor_config.EXIT_CHANNEL, new_state=SensorState.CLEARED)
                    asyncio.create_task(self.event_callback(event))

            await asyncio.sleep(self.polling_interval_sec)
```

---

### `app/core/camera_manager.py`

```python
"""
REVISED: The `capture_and_save_image` method is now more robust.
- It no longer just checks if the frame queue is empty.
- It now actively waits for up to 1 second for a new frame to arrive before
  timing out. This resolves the race condition where slower cameras (like USB)
  wouldn't have a frame ready in time for an event capture.
"""
import asyncio
import time
import redis.asyncio as redis
from enum import Enum
from typing import Optional, Dict, Set
import cv2
import numpy as np
from pathlib import Path

from redis import exceptions as redis_exceptions
from app.services.notification_service import AsyncNotificationService
from config import ACTIVE_CAMERA_IDS

class CameraHealthStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class AsyncCameraManager:
    def __init__(self, notification_service: AsyncNotificationService, captures_dir: str):
        self.redis_client = redis.from_url("redis://localhost")
        self._notification_service = notification_service
        self._captures_dir_base = Path(captures_dir)
        self._listener_tasks: Dict[str, asyncio.Task] = {}
        self._health_status: Dict[str, CameraHealthStatus] = {cam_id: CameraHealthStatus.DISCONNECTED for cam_id in ACTIVE_CAMERA_IDS}
        self._frame_queues: Dict[str, asyncio.Queue] = {cam_id: asyncio.Queue(maxsize=5) for cam_id in ACTIVE_CAMERA_IDS}
        self._stream_listeners: Dict[str, Set[asyncio.Queue]] = {cam_id: set() for cam_id in ACTIVE_CAMERA_IDS}
        self._last_event_image_paths: Dict[str, Optional[str]] = {cam_id: None for cam_id in ACTIVE_CAMERA_IDS}
        self._stream_lock = asyncio.Lock()

    def start(self):
        for cam_id in ACTIVE_CAMERA_IDS:
            if cam_id not in self._listener_tasks or self._listener_tasks[cam_id].done():
                self._listener_tasks[cam_id] = asyncio.create_task(self._redis_listener(cam_id))

    async def stop(self):
        for task in self._listener_tasks.values():
            if task and not task.done():
                task.cancel()
        await self.redis_client.close()

    async def _redis_listener(self, cam_id: str):
        channel_name = f"camera:frames:{cam_id}"
        while True:
            try:
                async with self.redis_client.pubsub() as pubsub:
                    await pubsub.subscribe(channel_name)
                    while True:
                        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5.0)
                        if message:
                            self._health_status[cam_id] = CameraHealthStatus.CONNECTED
                            frame_data = message['data']
                            # Clear old frames before adding a new one to keep it fresh
                            while not self._frame_queues[cam_id].empty():
                                self._frame_queues[cam_id].get_nowait()
                            self._frame_queues[cam_id].put_nowait(frame_data)
                            async with self._stream_lock:
                                for queue in self._stream_listeners[cam_id]:
                                    if not queue.full():
                                        queue.put_nowait(frame_data)
                        else:
                            if self._health_status.get(cam_id) == CameraHealthStatus.CONNECTED:
                                await self._notification_service.send_alert("WARNING", f"Camera '{cam_id}' has stopped publishing frames.")
                            self._health_status[cam_id] = CameraHealthStatus.DISCONNECTED
            except redis_exceptions.ConnectionError as e:
                self._health_status[cam_id] = CameraHealthStatus.ERROR
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                break
            except Exception:
                self._health_status[cam_id] = CameraHealthStatus.ERROR
                await asyncio.sleep(10)
    
    async def start_stream(self, cam_id: str) -> Optional[asyncio.Queue]:
        if cam_id not in ACTIVE_CAMERA_IDS: return None
        q = asyncio.Queue(maxsize=2)
        async with self._stream_lock:
            self._stream_listeners[cam_id].add(q)
        return q

    async def stop_stream(self, cam_id: str, queue: asyncio.Queue):
        if cam_id not in ACTIVE_CAMERA_IDS: return
        async with self._stream_lock:
            self._stream_listeners[cam_id].discard(queue)

    async def capture_and_save_image(self, cam_id: str, filename_prefix: str) -> Optional[str]:
        if self._health_status.get(cam_id) != CameraHealthStatus.CONNECTED:
            print(f"Cannot capture image from '{cam_id}': camera not connected.")
            return None
        
        try:
            # --- THE CRITICAL FIX ---
            # Wait for a new frame for up to 1.0 second.
            # This prevents the race condition with slower cameras.
            print(f"Waiting for frame from '{cam_id}'...")
            jpeg_bytes = await asyncio.wait_for(self._frame_queues[cam_id].get(), timeout=1.0)
            self._frame_queues[cam_id].task_done()
            print(f"Frame received from '{cam_id}'. Saving image...")

            captures_dir = self._captures_dir_base / cam_id
            captures_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{filename_prefix}_{int(time.time())}.jpg"
            full_path = captures_dir / filename
            
            def save_image_sync():
                np_array = np.frombuffer(jpeg_bytes, np.uint8)
                img_decoded = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                if img_decoded is None: return None
                cv2.imwrite(str(full_path), img_decoded)
                return f"/captures/{cam_id}/{filename}"
            
            web_path = await asyncio.to_thread(save_image_sync)
            if web_path:
                self._last_event_image_paths[cam_id] = web_path
            return web_path
            
        except asyncio.TimeoutError:
            print(f"Error saving image for '{cam_id}': Timed out waiting for a frame.")
            return None
        except Exception as e:
            print(f"Error saving image for '{cam_id}': {e}")
            return None

    def get_health_status(self, cam_id: str) -> CameraHealthStatus:
        return self._health_status.get(cam_id, CameraHealthStatus.DISCONNECTED)

    def get_all_health_statuses(self) -> Dict[str, str]:
        return {cam_id: status.value for cam_id, status in self._health_status.items()}

    def get_last_event_image_path(self, cam_id: str) -> Optional[str]:
        return self._last_event_image_paths.get(cam_id)
```

---

### `app/core/modbus_controller.py`

```python
"""
NEW: Modbus Hardware Controller
This class is the single source of truth for all Modbus RTU communication.
It handles connections and provides low-level methods to read and write
to the two different USR-IO modules on the RS485 bus.
"""
import asyncio
from enum import Enum
from typing import Optional, List
from pymodbus.client import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.framer import ModbusRtuFramer

from config import settings


class ModbusHealthStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
    DISCONNECTED = "disconnected"


class AsyncModbusController:
    _instance: Optional['AsyncModbusController'] = None
    _lock = asyncio.Lock()

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._config = settings.MODBUS
            self.client = AsyncModbusSerialClient(
                port=self._config.PORT,
                framer=ModbusRtuFramer,
                baudrate=self._config.BAUDRATE,
                bytesize=8,
                parity="N",
                stopbits=1,
                timeout=self._config.TIMEOUT_SEC,
            )
            self.initialized = True
            self.health_status = ModbusHealthStatus.DISCONNECTED
            self._is_connected = False
            
            # --- THE DEFINITIVE FIX IS HERE ---
            # The API sends lowercase names (e.g., 'camera_light'). The original code created a map
            # with uppercase keys ('CAMERA_LIGHT'), causing the lookup to fail.
            # This comprehension creates the map with lowercase keys to ensure a match.
            self._output_name_to_address_map = {
                k.lower(): v for k, v in settings.OUTPUTS.model_dump().items()
            }
            self._output_address_to_name_map = {v: k for k, v in self._output_name_to_address_map.items()}
            print("--- Modbus Controller Initialized ---")
            print(f"    Loaded output map: {self._output_name_to_address_map}")


    @classmethod
    async def get_instance(cls) -> 'AsyncModbusController':
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def get_output_address(self, name: str) -> Optional[int]:
        # Now, the lookup `name.lower()` will correctly find keys like 'camera_light' in our map.
        return self._output_name_to_address_map.get(name.lower())

    async def connect(self) -> bool:
        if self._is_connected:
            return True
        try:
            is_connected = await self.client.connect()
            if is_connected:
                print("Modbus Controller: Successfully connected to serial port.")
                self.health_status = ModbusHealthStatus.OK
                self._is_connected = True
                return True
            else:
                print("Modbus Controller: Failed to connect to serial port.")
                self.health_status = ModbusHealthStatus.DISCONNECTED
                self._is_connected = False
                return False
        except Exception as e:
            print(f"Modbus Controller: Error during connection attempt: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            self._is_connected = False
            return False

    async def disconnect(self):
        if self._is_connected:
            self.client.close()
            self._is_connected = False
            self.health_status = ModbusHealthStatus.DISCONNECTED
            print("Modbus Controller: Connection closed.")

    async def read_digital_inputs(self) -> Optional[List[bool]]:
        """Reads the 4 discrete inputs from the USR-IO4040 (Slave ID 1). FC=2, Address=0, Quantity=4."""
        if not await self.connect(): return None
        try:
            result = await self.client.read_discrete_inputs(
                address=0, count=4, slave=self._config.DEVICE_ADDRESS_INPUTS
            )
            if result.isError(): raise ModbusIOException(f"Modbus error on input read: {result}")
            
            # --- THE BUG FIX IS HERE ---
            # The library might return a list shorter than 4. We must pad it.
            # The default state for an NPN sensor input is HIGH (True).
            bits = result.bits
            while len(bits) < 4:
                bits.append(True)
            return bits[:4]
            # --- END OF FIX ---

        except (ConnectionException, ModbusIOException, asyncio.TimeoutError) as e:
            print(f"Modbus read_digital_inputs failed: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            await self.disconnect()
            return None

    async def read_coils(self) -> Optional[List[bool]]:
        """Reads the 8 relay statuses from the USR-IO8000 (Slave ID 2). FC=1, Address=0, Quantity=8."""
        if not await self.connect(): return None
        try:
            result = await self.client.read_coils(
                address=0, count=8, slave=self._config.DEVICE_ADDRESS_OUTPUTS
            )
            if result.isError(): raise ModbusIOException(f"Modbus error on coil read: {result}")

            # --- APPLYING THE SAME FIX FOR ROBUSTNESS ---
            # The default state for an output coil is OFF (False).
            bits = result.bits
            while len(bits) < 8:
                bits.append(False)
            return bits[:8]
            # --- END OF FIX ---

        except (ConnectionException, ModbusIOException, asyncio.TimeoutError) as e:
            print(f"Modbus read_coils failed: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            await self.disconnect()
            return None

    async def write_coil(self, address: int, state: bool) -> bool:
        """Writes a single coil (relay) on the USR-IO8000 (Slave ID 2). FC=5."""
        if not await self.connect(): return False
        try:
            result = await self.client.write_coil(
                address=address, value=state, slave=self._config.DEVICE_ADDRESS_OUTPUTS
            )
            if result.isError(): raise ModbusIOException(f"Modbus error on coil write: {result}")
            return True
        except (ConnectionException, ModbusIOException, asyncio.TimeoutError) as e:
            print(f"Modbus write_coil failed for address {address}: {e}")
            self.health_status = ModbusHealthStatus.ERROR
            await self.disconnect()
            return False
```

---

### `app/core/system_orchestrator.py`

```python
"""
Conceptual System Orchestrator
In our current design, the FastAPI lifespan manager in `main.py` acts as the
primary orchestrator. This file serves as a conceptual model for how more complex,
multi-service workflows could be managed.
"""
import asyncio

from .gpio_controller import AsyncGPIOController
from .camera_manager import AsyncCameraManager
from app.services.detection_service import AsyncDetectionService
from app.services.notification_service import AsyncNotificationService

class SystemOrchestrator:
    """
    A high-level class to coordinate major system operations.
    """
    def __init__(
        self,
        gpio: AsyncGPIOController,
        camera: AsyncCameraManager,
        detection: AsyncDetectionService,
        notifier: AsyncNotificationService,
    ):
        self.gpio = gpio
        self.camera = camera
        self.detection = detection
        self.notifier = notifier

    async def run_full_diagnostic_sequence(self):
        """
        An example of a complex workflow that involves multiple services.
        """
        print("Orchestrator: Starting full system diagnostic...")
        await self.notifier.send_alert("INFO", "Starting system diagnostics.")
        
        # Step 1: Check hardware
        gpio_health = await self.gpio.health_check()
        camera_health = await self.camera.health_check()
        
        # Step 2: Test hardware functions
        await self.gpio.beep(0.1)
        await self.gpio.blink_led("led_green", 0.1, 0) # Quick flash
        
        # Step 3: Log results
        print(f"Diagnostics complete: GPIO={gpio_health.value}, Camera={camera_health.value}")
        await self.notifier.send_alert("INFO", "Diagnostics complete.", {
            "gpio": gpio_health.value,
            "camera": camera_health.value
        })

    async def perform_safe_shutdown(self):
        """
        An orchestrated shutdown sequence.
        """
        print("Orchestrator: Performing safe shutdown.")
        await self.notifier.send_alert("WARNING", "System is shutting down.")
        await self.gpio.stop_conveyor()
        await self.gpio.close_gate() # Assuming a gate exists
        await self.gpio.shutdown()
        await self.camera.stop_capture()

```

---

### `app/core/sensor_events.py`

```python
"""
Phase 2.2: Event Handling System for Sensors
Defines the data structures for sensor events using Pydantic for validation
and Enums for clear state representation.
"""
import time
from enum import Enum
from pydantic import BaseModel, Field

class SensorState(str, Enum):
    """Represents the state of a single sensor."""
    TRIGGERED = "triggered" # Object detected
    CLEARED = "cleared"   # No object detected

class SensorEvent(BaseModel):
    """Data model for a sensor state change event."""
    sensor_id: int
    new_state: SensorState
    timestamp: float = Field(default_factory=time.monotonic)

```

---

### `app/utils/__init__.py`

```python
# This file is empty.

```

---

### `app/web/__init__.py`

```python
# This file is empty.

```

---

### `app/web/router.py`

```python
"""
Web routes for serving HTML pages.
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pathlib import Path
import markdown2 # <-- NEW: Import the markdown library

from app.models import get_async_session, EventLog, ObjectProfile
from config import settings, ACTIVE_CAMERA_IDS

router = APIRouter(tags=["Web Dashboard"])
PROJECT_ROOT = Path(__file__).parent.parent.parent # Define project root

def NoCacheTemplateResponse(request: Request, name: str, context: dict):
    """A helper that adds no-cache headers and injects global context."""
    templates = request.app.state.templates
    context['active_camera_ids'] = ACTIVE_CAMERA_IDS
    context['camera_profiles'] = getattr(request.app.state, 'camera_profiles', [])
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    return templates.TemplateResponse(name, context, headers=headers)

# ... (all existing routes like @router.get("/"), @router.get("/management/recipes"), etc.)
# ... (They are unchanged, so I am omitting them for brevity)

@router.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(ObjectProfile).order_by(ObjectProfile.name))
    object_profiles = result.scalars().all()
    context = {"request": request, "object_profiles": object_profiles, "animation_time": settings.UI_ANIMATION_TRANSIT_TIME_SEC}
    return NoCacheTemplateResponse(request, "dashboard.html", context)

@router.get("/management/recipes", response_class=HTMLResponse)
async def read_profiles_page(request: Request):
    return NoCacheTemplateResponse(request, "profiles.html", {"request": request})

@router.get("/management/products", response_class=HTMLResponse)
async def read_products_page(request: Request):
    return NoCacheTemplateResponse(request, "products.html", {"request": request})

@router.get("/management/operators", response_class=HTMLResponse)
async def read_operators_page(request: Request):
    return NoCacheTemplateResponse(request, "operators.html", {"request": request})

@router.get("/status", response_class=HTMLResponse)
async def read_status_page(request: Request):
    return NoCacheTemplateResponse(request, "status.html", {"request": request})

@router.get("/hardware", response_class=HTMLResponse)
async def read_hardware_page(request: Request):
    return NoCacheTemplateResponse(request, "hardware.html", {"request": request, "config": settings})
    
@router.get("/run-history", response_class=HTMLResponse)
async def read_run_history_page(request: Request):
    return NoCacheTemplateResponse(request, "run_history.html", {"request": request})

# --- THIS IS THE NEW FEATURE ---
@router.get("/help/{page_name}", response_class=HTMLResponse)
async def read_help_page(request: Request, page_name: str):
    """
    Reads a markdown file from the docs/manuals directory, converts it to HTML,
    and renders it in a template.
    """
    # Sanitize page_name to prevent directory traversal attacks
    if ".." in page_name or "/" in page_name:
        raise HTTPException(status_code=404, detail="Help page not found.")

    file_path = PROJECT_ROOT / "docs" / "manuals" / f"{page_name}.md"
    
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Help page not found.")
        
    # Read markdown content
    markdown_text = file_path.read_text()
    
    # Convert to HTML
    html_content = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables", "admonitions"])
    
    # Capitalize the title for display
    title = page_name.replace("_", " ").capitalize()
    
    context = {"request": request, "title": title, "content": html_content}
    return NoCacheTemplateResponse(request, "help.html", context)
# --- END OF NEW FEATURE ---

# ... (all other existing routes like camera views, logs, etc.)
# ... (They are also unchanged)
@router.get("/connections", response_class=HTMLResponse)
async def read_connections_page(request: Request):
    return NoCacheTemplateResponse(request, "connections.html", {"request": request, "config": settings})

if 'rpi' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/rpi", response_class=HTMLResponse)
    async def read_live_view_rpi(request: Request):
        return NoCacheTemplateResponse(request, "live_view_rpi.html", {"request": request})
    @router.get("/gallery/rpi", response_class=HTMLResponse)
    async def read_gallery_rpi(request: Request):
        context = {"request": request, "camera_id": "rpi", "camera_name": "RPi"}
        return NoCacheTemplateResponse(request, "gallery.html", context)

if 'usb' in ACTIVE_CAMERA_IDS:
    @router.get("/live-view/usb", response_class=HTMLResponse)
    async def read_live_view_usb(request: Request):
        return NoCacheTemplateResponse(request, "live_view_usb.html", {"request": request})
    @router.get("/gallery/usb", response_class=HTMLResponse)
    async def read_gallery_usb(request: Request):
        context = {"request": request, "camera_id": "usb", "camera_name": "USB"}
        return NoCacheTemplateResponse(request, "gallery.html", context)

@router.get("/logs", response_class=HTMLResponse)
async def read_logs_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(EventLog).order_by(EventLog.timestamp.desc()).limit(100))
    logs = result.scalars().all()
    context = {"request": request, "logs": logs}
    return NoCacheTemplateResponse(request, "logs.html", context)

@router.get("/api-docs", response_class=HTMLResponse)
async def read_api_docs_page(request: Request):
    openapi_schema = request.app.openapi()
    context = {"request": request, "api_title": openapi_schema.get("info", {}).get("title", "API"), "api_version": openapi_schema.get("info", {}).get("version", ""), "api_paths": openapi_schema.get("paths", {})}
    return NoCacheTemplateResponse(request, "api.html", context)
```

---

### `app/services/__init__.py`

```python
# This file is empty.

```

---

### `app/services/detection_service.py`

```python
"""
Manages the detection and counting workflow.
"""
import asyncio
import uuid
from collections import deque
from typing import Dict, Deque

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager
from app.core.sensor_events import SensorEvent, SensorState
from app.services.orchestration_service import AsyncOrchestrationService, OperatingMode
from app.models.database import AsyncSessionFactory
from app.models.detection import DetectionEventLog
from config import ACTIVE_CAMERA_IDS, settings

class AsyncDetectionService:
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        camera_manager: AsyncCameraManager,
        orchestration_service: AsyncOrchestrationService,
        conveyor_settings,
        db_session_factory
    ):
        self._io = modbus_controller
        self._camera_manager = camera_manager
        self._orchestration = orchestration_service
        self._conveyor_config = conveyor_settings
        self._get_db_session = db_session_factory
        self._lock = asyncio.Lock()
        self._verbose = settings.LOGGING.VERBOSE_LOGGING
        self._output_map = settings.OUTPUTS

        self._in_flight_objects: Deque[str] = deque()
        self._entry_timestamps: Dict[int, float] = {}
        self._stalled_product_timers: Dict[str, asyncio.TimerHandle] = {}
        
        self._base_travel_time_sec = 0.0
        if self._conveyor_config.SPEED_M_PER_SEC > 0:
            self._base_travel_time_sec = self._conveyor_config.CAMERA_TO_SORTER_DISTANCE_M / self._conveyor_config.SPEED_M_PER_SEC
        print(f"Detection Service: Calculated base travel time of {self._base_travel_time_sec:.2f} seconds.")

    def get_in_flight_count(self) -> int:
        return len(self._in_flight_objects)

    async def _check_sensor_block_time(self, event: SensorEvent):
        start_time = self._entry_timestamps.pop(event.sensor_id, None)
        if start_time is None: return
        block_duration_ms = (event.timestamp - start_time) * 1000
        active_profile = self._orchestration.get_active_profile()
        if not (active_profile and active_profile.product): return
        product = active_profile.product
        min_time, max_time = product.min_sensor_block_time_ms, product.max_sensor_block_time_ms
        if min_time is not None and max_time is not None and not (min_time <= block_duration_ms <= max_time):
            warning_msg = f"Product size mismatch! Blocked for {block_duration_ms:.0f}ms. Expected: {min_time}-{max_time}ms."
            await self._orchestration.trigger_persistent_alarm(warning_msg)
            if self._verbose: print(f"VALIDATION: {warning_msg}")

    async def _handle_stalled_product(self, box_id: str):
        async with self._lock:
            self._stalled_product_timers.pop(box_id, None)
            if box_id in self._in_flight_objects:
                self._in_flight_objects.remove(box_id)
                reason = f"Stalled product detected on conveyor (ID: {box_id})"
                print(f"DETECTION FAILURE: {reason}. Triggering run failure.")
                await self._orchestration.trigger_run_failure(reason)
            elif self._verbose:
                print(f"Stalled product timer fired for already processed Box ID {box_id}. Ignoring.")

    async def handle_sensor_event(self, event: SensorEvent):
        """The entry point for all sensor events from the Modbus Poller."""
        async with self._lock:
            # THIS IS THE SYNTAX FIX: This condition was previously malformed.
            # It now correctly checks if the mode is NOT one of the active states.
            if self._orchestration.get_status()["mode"] not in [OperatingMode.RUNNING.value, OperatingMode.POST_RUN_DELAY.value]:
                if self._stalled_product_timers:
                    for timer in self._stalled_product_timers.values():
                        timer.cancel()
                    self._stalled_product_timers.clear()
                return

            if event.sensor_id == settings.SENSORS.ENTRY_CHANNEL:
                if event.new_state == SensorState.TRIGGERED:
                    # Don't log a new box if the system is in the post-run delay phase
                    if self._orchestration.get_status()["mode"] != OperatingMode.RUNNING.value:
                        return
                        
                    self._entry_timestamps[event.sensor_id] = event.timestamp
                    box_id = str(uuid.uuid4())
                    self._in_flight_objects.append(box_id)
                    
                    timeout_sec = self._conveyor_config.MAX_TRANSIT_TIME_SEC
                    loop = asyncio.get_running_loop()
                    timer_handle = loop.call_later(
                        timeout_sec,
                        lambda: asyncio.create_task(self._handle_stalled_product(box_id))
                    )
                    self._stalled_product_timers[box_id] = timer_handle
                    
                    if self._verbose: print(f"DETECTION: New box ID {box_id}. Stalled timer set for {timeout_sec}s.")
                    
                    if settings.CAMERA_TRIGGER_DELAY_MS > 0:
                        await asyncio.sleep(settings.CAMERA_TRIGGER_DELAY_MS / 1000.0)
                    
                    image_path = None
                    if ACTIVE_CAMERA_IDS:
                        image_path = await self._camera_manager.capture_and_save_image(ACTIVE_CAMERA_IDS[0], f'event_{box_id}')
                    
                    active_run_id = self._orchestration.get_active_run_id()
                    if active_run_id:
                        try:
                            async with self._get_db_session() as session:
                                new_event = DetectionEventLog(run_log_id=active_run_id, image_path=image_path)
                                session.add(new_event)
                                await session.commit()
                        except Exception as e:
                            print(f"ERROR: Could not log detection event to database: {e}")
                
                elif event.new_state == SensorState.CLEARED:
                    await self._check_sensor_block_time(event)

            elif event.sensor_id == settings.SENSORS.EXIT_CHANNEL and event.new_state == SensorState.TRIGGERED:
                if self._in_flight_objects:
                    exiting_box_id = self._in_flight_objects.popleft()
                    
                    timer_to_cancel = self._stalled_product_timers.pop(exiting_box_id, None)
                    if timer_to_cancel:
                        timer_to_cancel.cancel()
                        if self._verbose: print(f"DETECTION: Box {exiting_box_id} confirmed exit. Stalled timer cancelled.")
                    
                    await self._orchestration.on_exit_sensor_triggered()
                    await self._orchestration.on_box_processed()
                else:
                    print("DETECTION WARNING: Exit sensor triggered, but no objects were tracked in-flight.")
```

---

### `app/services/notification_service.py`

```python
"""
REVISED: The notification service is now simplified and has no direct hardware control.
- The `gpio_controller` dependency has been completely removed.
- Its only responsibilities are printing alerts and logging them to the database.
"""
import asyncio
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel

# Removed the obsolete import for AsyncGPIOController
from app.models.event_log import EventLog, EventType

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class Alert(BaseModel):
    level: AlertLevel
    message: str
    details: Optional[Dict[str, Any]] = None

class AsyncNotificationService:
    # --- THE FIX IS HERE ---
    # The `gpio_controller` argument has been removed from the __init__ method.
    def __init__(self, db_session_factory):
        # The self._gpio attribute has been removed.
        self._get_db_session = db_session_factory
        self._queue = asyncio.Queue(maxsize=100)
        self._worker_task: Optional[asyncio.Task] = None

    def start(self):
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._notification_worker())

    def stop(self):
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()

    async def send_alert(self, level: str, message: str, details: Optional[dict] = None):
        try:
            alert_level = AlertLevel(level.lower())
            alert = Alert(level=alert_level, message=message, details=details)
            self._queue.put_nowait(alert)
        except asyncio.QueueFull:
            print("Notification Service Warning: Alert queue is full. Dropping oldest alert.")
            await self._queue.get()
            await self._queue.put(alert)

    async def _notification_worker(self):
        while True:
            try:
                alert: Alert = await self._queue.get()
                # 1. Print to console
                print(f"Notification: [{alert.level.name}] {alert.message}")

                # 2. Persist the log to the database
                await self._log_event_to_db(alert)

                # --- The physical notification logic (blinking LEDs) has been removed ---
                # This is because this service no longer controls hardware.
                # The OrchestrationService is now responsible for status lights.

                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in notification worker: {e}")

    async def _log_event_to_db(self, alert: Alert):
        try:
            async with self._get_db_session() as session:
                log_entry = EventLog(
                    event_type=EventType(alert.level.value),
                    source="SYSTEM", # Could be enhanced to be more specific
                    message=alert.message,
                    details=alert.details
                )
                session.add(log_entry)
                await session.commit()
        except Exception as e:
            print(f"Failed to log event to database: {e}")
```

---

### `app/services/system_service.py`

```python
"""
Provides high-level system monitoring and control functionality.

REVISED: All AI-related status information has been removed from the
system status payload.

DEFINITIVE FIX: The __init__ method is corrected to only accept the
dependencies it actually uses, resolving the startup TypeError.
"""
import time
from typing import Dict, Optional
import psutil

from app.core.modbus_controller import AsyncModbusController
from app.core.camera_manager import AsyncCameraManager, CameraHealthStatus
from app.core.modbus_poller import AsyncModbusPoller
from app.services.orchestration_service import AsyncOrchestrationService
from app.services.detection_service import AsyncDetectionService
from config import ACTIVE_CAMERA_IDS
from config.settings import AppSettings # Import for type hinting

def _get_rpi_cpu_temp() -> Optional[float]:
    """Safely gets the Raspberry Pi CPU temperature."""
    try:
        temps = psutil.sensors_temperatures()
        return temps.get('cpu_thermal', [None])[0].current if temps else None
    except Exception:
        return None

class AsyncSystemService:
    """
    Gathers and provides a unified status report for all system components.
    """
    # --- THIS IS THE CORRECTED CONSTRUCTOR ---
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        modbus_poller: AsyncModbusPoller,
        camera_manager: AsyncCameraManager,
        detection_service: AsyncDetectionService,
        orchestration_service: AsyncOrchestrationService,
        settings: AppSettings # <-- It still needs the main settings
    ):
        self._io = modbus_controller
        self._poller = modbus_poller
        self._camera = camera_manager
        self._detection_service = detection_service
        self._orchestration_service = orchestration_service
        self._settings = settings # <-- Use the injected settings
        self._sensor_config = self._settings.SENSORS
        self._output_config = self._settings.OUTPUTS.model_dump()
        self._app_start_time = time.monotonic()

    async def full_system_reset(self):
        """Resets the running process. This is a "soft" reset."""
        await self._orchestration_service.stop_run()

    async def get_system_status(self) -> Dict:
        """Gathers the current health status from all components safely."""
        try:
            all_camera_statuses = self._camera.get_all_health_statuses()
            camera_statuses_payload = {
                cam_id: all_camera_statuses.get(cam_id, CameraHealthStatus.DISCONNECTED.value)
                for cam_id in ACTIVE_CAMERA_IDS
            }
            io_module_status = self._poller.get_io_health().value
            input_states = self._poller.get_current_input_states()
            output_states = self._poller.get_current_output_states()

            def get_input_state(channel: int) -> bool:
                """Safely gets the raw boolean state for a 1-based channel number."""
                index = channel - 1
                if 0 <= index < len(input_states):
                    return input_states[index]
                return True 

            def get_output_state(name: str) -> bool:
                """Safely get the boolean state for a named output."""
                channel = self._output_config.get(name.upper())
                if channel is not None and 0 <= channel < len(output_states):
                    return output_states[channel]
                return False

            return {
                "cpu_usage": psutil.cpu_percent(interval=None),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "cpu_temperature": _get_rpi_cpu_temp(),
                "uptime_seconds": int(time.monotonic() - self._app_start_time),
                "camera_statuses": camera_statuses_payload,
                "io_module_status": io_module_status,
                "sensor_1_status": not get_input_state(self._sensor_config.ENTRY_CHANNEL), 
                "sensor_2_status": not get_input_state(self._sensor_config.EXIT_CHANNEL), 
                "conveyor_relay_status": get_output_state("conveyor"),
                "gate_relay_status": get_output_state("gate"),
                "diverter_relay_status": get_output_state("diverter"),
                "led_green_status": get_output_state("led_green"),
                "led_red_status": get_output_state("led_red"),
                "buzzer_status": get_output_state("buzzer"),
                "camera_light_status": get_output_state("camera_light"),
                "in_flight_count": self._detection_service.get_in_flight_count(),
            }
        except Exception as e:
            print(f"FATAL ERROR in get_system_status: {e}")
            return {"error": "Failed to fetch system status."}

    async def emergency_stop(self):
        """Immediately stop all hardware operations via Modbus."""
        print("SYSTEM SERVICE: Initiating emergency stop of all hardware.")
        await self._io.write_coil(self._output_config.get("CONVEYOR"), False)
        await self._io.write_coil(self._output_config.get("GATE"), False)
        await self._io.write_coil(self._output_config.get("DIVERTER"), False)
        await self._io.write_coil(self._output_config.get("LED_GREEN"), False)
        await self._io.write_coil(self._output_config.get("LED_RED"), True)
        await self._io.write_coil(self._output_config.get("CAMERA_LIGHT"), False)
```

---

### `app/services/orchestration_service.py`

```python
"""
Service for controlling the high-level orchestration of production runs.
"""
import asyncio
import json
from enum import Enum
from typing import Optional, Any, Dict
from datetime import datetime

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.modbus_controller import AsyncModbusController
from app.models.profiles import ObjectProfile, Product
from app.models.run_log import RunLog, RunStatus
from app.models.event_log import EventLog, EventType
from config import ACTIVE_CAMERA_IDS, settings
from config.settings import AppSettings


class OperatingMode(str, Enum):
    STOPPED = "Stopped"
    IDLE = "Idle"
    RUNNING = "Running"
    PAUSED_BETWEEN_BATCHES = "Paused (Between Batches)"
    POST_RUN_DELAY = "Post-Run Delay"

class AsyncOrchestrationService:
    def __init__(
        self,
        modbus_controller: AsyncModbusController,
        db_session_factory,
        redis_client: redis.Redis,
        app_settings: AppSettings
    ):
        self._io = modbus_controller
        self._get_db_session = db_session_factory
        self._redis = redis_client
        self._settings = app_settings
        self._mode = OperatingMode.STOPPED
        self._lock = asyncio.Lock()
        
        self._active_profile: Optional[ObjectProfile] = None
        self._active_product: Optional[Product] = None
        self._active_run_id: Optional[int] = None
        self._active_alarm_message: Optional[str] = None

        self._run_profile_id: Optional[int] = None
        self._run_batch_code: Optional[str] = None
        self._run_operator_id: Optional[int] = None
        self._run_target_count: int = 0
        self._run_post_batch_delay_sec: int = 5
        self._current_count: int = 0
        
        self._output_map = self._settings.OUTPUTS

    async def _trigger_timed_beep(self, duration_sec: float):
        """Asynchronously triggers the buzzer for a specific duration."""
        if duration_sec <= 0:
            return
        try:
            await self._io.write_coil(self._output_map.BUZZER, True)
            await asyncio.sleep(duration_sec)
            await self._io.write_coil(self._output_map.BUZZER, False)
        except Exception as e:
            print(f"Buzzer Error: {e}")

    def beep_for(self, duration_ms: int):
        """Creates a background task for a non-blocking beep."""
        duration_sec = duration_ms / 1000.0
        asyncio.create_task(self._trigger_timed_beep(duration_sec))

    async def initialize_hardware_state(self):
        print("Orchestrator: Setting initial hardware state to STOPPED.")
        await self._io.write_coil(self._output_map.GATE, False)
        await self._io.write_coil(self._output_map.DIVERTER, False)
        await self._io.write_coil(self._output_map.CONVEYOR, False)
        await self._io.write_coil(self._output_map.LED_GREEN, False)
        await self._io.write_coil(self._output_map.LED_RED, True)
        await self._io.write_coil(self._output_map.BUZZER, False)

    def get_active_profile(self) -> Optional[ObjectProfile]:
        return self._active_profile

    def get_active_run_id(self) -> Optional[int]:
        return self._active_run_id

    async def on_box_processed(self):
        task_to_run = None
        async with self._lock:
            if self._mode == OperatingMode.RUNNING:
                self._current_count += 1
                if self._run_target_count > 0 and self._current_count >= self._run_target_count:
                    print("Orchestrator: Target count reached. Beginning stop delay sequence.")
                    task_to_run = asyncio.create_task(self.complete_and_loop_run())
        if task_to_run:
            await task_to_run

    async def on_exit_sensor_triggered(self):
        """Triggers a short beep when the exit sensor is hit."""
        self.beep_for(self._settings.BUZZER.EXIT_SENSOR_MS)

    async def trigger_persistent_alarm(self, message: str):
        self.beep_for(self._settings.BUZZER.MISMATCH_MS)
        if self._active_alarm_message: return
        self._active_alarm_message = message
        print(f"ORCHESTRATION ALARM: {message}")
        try:
            async with self._get_db_session() as session:
                log_entry = EventLog(
                    event_type=EventType.WARNING, source="ORCHESTRATION", message=message,
                    details={"run_log_id": self._active_run_id, "batch_code": self._run_batch_code}
                )
                session.add(log_entry)
                await session.commit()
        except Exception as e:
            print(f"Failed to log alarm to database: {e}")

    async def trigger_run_failure(self, reason: str):
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            print(f"CRITICAL RUN FAILURE: {reason}. Stopping all operations.")
            try:
                async with self._get_db_session() as session:
                    log_entry = EventLog(
                        event_type=EventType.ERROR, source="SYSTEM_FAILURE", message=reason,
                        details={"run_log_id": self._active_run_id, "batch_code": self._run_batch_code}
                    )
                    session.add(log_entry)
                    await session.commit()
            except Exception as e:
                print(f"Failed to log critical failure to database: {e}")
            await self._update_run_log_status(RunStatus.FAILED)
            self._mode = OperatingMode.STOPPED
            self._active_profile, self._active_product, self._active_run_id = None, None, None
            self._run_profile_id, self._current_count, self._run_target_count = None, 0, 0
            await self._io.write_coil(self._output_map.CONVEYOR, False)
            await self._io.write_coil(self._output_map.GATE, False)
            await self._io.write_coil(self._output_map.DIVERTER, False)
            await self._io.write_coil(self._output_map.LED_GREEN, False)
            await self._io.write_coil(self._output_map.LED_RED, True)
            await self.trigger_persistent_alarm(f"CRITICAL FAILURE: {reason}")

    async def acknowledge_alarm(self):
        if not self._active_alarm_message: return
        print(f"Orchestrator: Alarm '{self._active_alarm_message}' acknowledged by user.")
        self._active_alarm_message = None

    async def start_run(self, profile_id: int, target_count: int, post_batch_delay_sec: int, batch_code: str, operator_id: int) -> bool:
        async with self._lock:
            if self._mode in [OperatingMode.RUNNING, OperatingMode.PAUSED_BETWEEN_BATCHES, OperatingMode.POST_RUN_DELAY]:
                return False
            self._run_profile_id, self._run_target_count, self._run_post_batch_delay_sec, self._run_batch_code, self._run_operator_id = \
                profile_id, target_count, post_batch_delay_sec, batch_code, operator_id
            return await self._execute_start_sequence()
            
    async def _execute_start_sequence(self) -> bool:
        """Internal method to start a batch. Can be called to loop."""
        async with self._get_db_session() as session:
            result = await session.execute(
                select(ObjectProfile).options(selectinload(ObjectProfile.camera_profile), selectinload(ObjectProfile.product))
                .where(ObjectProfile.id == self._run_profile_id)
            )
            profile = result.scalar_one_or_none()
        if not profile or not profile.camera_profile: return False
        try:
            async with self._get_db_session() as session:
                profile_snapshot = {"object_profile_name": profile.name, "product_name": profile.product.name if profile.product else "N/A"}
                new_run_log = RunLog(
                    batch_code=self._run_batch_code, operator_id=self._run_operator_id, product_id=profile.product_id,
                    status=RunStatus.RUNNING, object_profile_snapshot=profile_snapshot
                )
                session.add(new_run_log); await session.commit(); await session.refresh(new_run_log)
                self._active_run_id = new_run_log.id
        except Exception as e:
            print(f"FATAL: Could not create RunLog in database. Aborting run. Error: {e}"); return False
            
        self._active_profile, self._active_product = profile, profile.product
        await self.acknowledge_alarm()

        # --- ADDED: Trigger a short beep to signal that the new run/loop is starting. ---
        # We use MANUAL_TOGGLE_MS as it's a good, short duration for a confirmation beep.
        self.beep_for(self._settings.BUZZER.MANUAL_TOGGLE_MS)

        print(f"Orchestrator: Loaded Active Profile -> '{profile.name}' for new batch. RunLog ID: {self._active_run_id}")
        cam_settings = profile.camera_profile
        command = {"action": "apply_settings", "settings": {"autofocus": cam_settings.autofocus, "exposure": cam_settings.exposure, "gain": cam_settings.gain, "white_balance_temp": cam_settings.white_balance_temp, "brightness": cam_settings.brightness}}
        for cam_id in ACTIVE_CAMERA_IDS:
            await self._redis.publish(f"camera:commands:{cam_id}", json.dumps(command))
        
        self._current_count, self._mode = 0, OperatingMode.RUNNING
        await self._io.write_coil(self._output_map.LED_RED, False)
        await self._io.write_coil(self._output_map.LED_GREEN, True)
        await self._io.write_coil(self._output_map.CONVEYOR, True)
        return True

    async def _update_run_log_status(self, status: RunStatus):
        if not self._active_run_id: return
        try:
            async with self._get_db_session() as session:
                run_log = await session.get(RunLog, self._active_run_id)
                if run_log:
                    run_log.status, run_log.end_timestamp = status, datetime.utcnow()
                    await session.commit()
        except Exception as e:
            print(f"Error updating RunLog status: {e}")

    async def complete_and_loop_run(self):
        """
        Sequence for when a batch target is met.
        """
        async with self._lock:
            if self._mode != OperatingMode.RUNNING: return
            
            await self._update_run_log_status(RunStatus.COMPLETED)
            
            # --- VERIFIED: This beep signals that the loop has completed its target. ---
            self.beep_for(self._settings.BUZZER.LOOP_COMPLETE_MS)
            
            self._mode = OperatingMode.POST_RUN_DELAY
            stop_delay = self._settings.CONVEYOR.CONVEYOR_AUTO_STOP_DELAY_SEC
            print(f"Orchestrator: Batch complete. Conveyor will stop in {stop_delay}s.")

        await asyncio.sleep(stop_delay)

        async with self._lock:
            if self._mode != OperatingMode.POST_RUN_DELAY: return
            await self._io.write_coil(self._output_map.CONVEYOR, False)
            self._mode = OperatingMode.PAUSED_BETWEEN_BATCHES
            pause_delay = self._run_post_batch_delay_sec
            print(f"Orchestrator: Conveyor stopped. Pausing for {pause_delay}s before next batch.")

        await asyncio.sleep(pause_delay)

        async with self._lock:
            if self._mode != OperatingMode.PAUSED_BETWEEN_BATCHES: return
            print("Orchestrator: Pause finished. Looping to next batch...")
            await self._execute_start_sequence()

    async def stop_run(self):
        async with self._lock:
            if self._mode == OperatingMode.STOPPED: return
            print("Orchestrator: STOP command received. Halting all operations.")
            if self._active_run_id and self._mode != OperatingMode.STOPPED:
                await self._update_run_log_status(RunStatus.ABORTED)
            self._mode = OperatingMode.STOPPED
            self._active_profile, self._active_product, self._active_run_id = None, None, None
            self._run_profile_id, self._current_count, self._run_target_count = None, 0, 0
            await self.acknowledge_alarm()
            await self.initialize_hardware_state()

    def get_status(self) -> dict:
        return {
            "mode": self._mode.value,
            "active_profile": self._active_profile.name if self._active_profile else "None",
            "run_progress": self._current_count,
            "target_count": self._run_target_count,
            "post_batch_delay_sec": self._run_post_batch_delay_sec,
            "active_alarm_message": self._active_alarm_message,
        }
```

---

### `app/models/__init__.py`

```python
# box_counter_system/app/models/__init__.py
"""
Makes key database components available for easy import.
This pattern simplifies imports for sessions, the base model class,
and all defined ORM models.
"""
from .database import Base, get_async_session, engine
from .detection import DetectionEventLog # MODIFIED: Renamed from Detection
from .system_status import SystemStatus
from .event_log import EventLog
from .configuration import Configuration
from .profiles import CameraProfile, ObjectProfile
from .product import Product, ProductStatus
from .operator import Operator, OperatorStatus
from .run_log import RunLog, RunStatus


__all__ = [
    "Base",
    "get_async_session",
    "engine",
    "DetectionEventLog", # MODIFIED: Export the new name
    "SystemStatus",
    "EventLog",
    "Configuration",
    "CameraProfile",
    "ObjectProfile",
    "Product",
    "ProductStatus",
    "Operator",
    "OperatorStatus",
    "RunLog",
    "RunStatus",
]
```

---

### `app/models/product.py`

```python
from sqlalchemy import Integer, String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column # Correctly import Mapped
from enum import Enum as PyEnum

from .database import Base

class ProductStatus(PyEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # --- THIS IS THE FIX ---
    # Changed 'Mpped' to the correct 'Mapped'
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    # -----------------------
    description: Mapped[str] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    ai_model_path: Mapped[str] = mapped_column(String(255), nullable=True, default="yolov8n.pt")
    min_sensor_block_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    max_sensor_block_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}')>"
```

---

### `app/models/run_log.py`

```python
from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Dict, List # Import List
from sqlalchemy import Integer, String, DateTime, Enum, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
from .operator import Operator
from .product import Product
# The relationship needs to know about the class, but we use a string to avoid circular imports
# from .detection import DetectionEventLog 

class RunStatus(PyEnum):
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    ABORTED = "Aborted by User"

class RunLog(Base):
    __tablename__ = "run_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    batch_code: Mapped[str] = mapped_column(String(100), index=True)
    start_timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    end_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.RUNNING)
    
    object_profile_snapshot: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    operator: Mapped["Operator"] = relationship()
    product: Mapped["Product"] = relationship()
    
    # New relationship to link to all detection events for this run
    detection_events: Mapped[List["DetectionEventLog"]] = relationship(back_populates="run")

    def __repr__(self) -> str:
        return f"<RunLog(id={self.id}, batch_code='{self.batch_code}', status='{self.status.name}')>"
```

---

### `app/models/event_log.py`

```python
from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Dict

from sqlalchemy import Integer, String, Text, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class EventType(PyEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class EventLog(Base):
    __tablename__ = "event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType))
    source: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<EventLog(id={self.id}, type={self.event_type}, source='{self.source}')>"

```

---

### `app/models/profiles.py`

```python
"""
NEW: Database models for storing dynamic camera and object profiles.
This allows for on-the-fly management of "recipes" for different
production runs.
"""
from typing import Optional
from sqlalchemy import Integer, String, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
# --- PHASE 1: Import Product for relationship ---
from .product import Product

class CameraProfile(Base):
    """
    Stores a complete set of hardware settings for a camera.
    This can be reused across multiple object profiles.
    """
    __tablename__ = "camera_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    # Camera hardware settings
    exposure: Mapped[int] = mapped_column(Integer, default=0)
    gain: Mapped[int] = mapped_column(Integer, default=0)
    white_balance_temp: Mapped[int] = mapped_column(Integer, default=0)
    brightness: Mapped[int] = mapped_column(Integer, default=128)
    autofocus: Mapped[bool] = mapped_column(Boolean, default=True)
    
    description: Mapped[Optional[str]] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"<CameraProfile(id={self.id}, name='{self.name}')>"


class ObjectProfile(Base):
    """
    The master "recipe" for a production run. It defines an object's
    name, its sorting logic, and links to a specific camera profile.
    """
    __tablename__ = "object_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    # Foreign key to link to a camera hardware configuration
    camera_profile_id: Mapped[int] = mapped_column(ForeignKey("camera_profiles.id"))
    
    # Sorting logic for this specific object
    sort_offset_ms: Mapped[int] = mapped_column(Integer, default=0, comment="Time adjustment in ms for sorting (+/- from base travel time)")
    
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # SQLAlchemy relationship to easily access the linked CameraProfile object
    camera_profile: Mapped["CameraProfile"] = relationship()
    
    # --- PHASE 1: Add relationship to the Product model ---
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id"), nullable=True)
    product: Mapped[Optional["Product"]] = relationship()


    def __repr__(self) -> str:
        return f"<ObjectProfile(id={self.id}, name='{self.name}')>"
```

---

### `app/models/system_status.py`

```python
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, Float, Boolean, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class CameraStatus(PyEnum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class GatePosition(PyEnum):
    OPEN = "open"
    CLOSED = "closed"
    MOVING = "moving"
    ERROR = "error"

class SystemStatus(Base):
    __tablename__ = "system_status_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    cpu_usage: Mapped[float] = mapped_column(Float)
    memory_usage: Mapped[float] = mapped_column(Float)
    disk_usage: Mapped[float] = mapped_column(Float)
    cpu_temperature: Mapped[float] = mapped_column(Float)
    
    camera_status: Mapped[CameraStatus] = mapped_column(Enum(CameraStatus))
    conveyor_running: Mapped[bool] = mapped_column(Boolean)
    gate_position: Mapped[GatePosition] = mapped_column(Enum(GatePosition))
    
    uptime_seconds: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"<SystemStatus(id={self.id}, time={self.timestamp})>"

```

---

### `app/models/detection.py`

```python
import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
# This import is needed for the relationship
from .run_log import RunLog

class DetectionEventLog(Base):
    """
    Records a single detection event within a production run.
    This creates a permanent link between a run and its captured images.
    """
    __tablename__ = "detection_event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign key to the run this detection belongs to
    run_log_id: Mapped[int] = mapped_column(ForeignKey("run_logs.id"), index=True)
    
    # The run this event belongs to
    run: Mapped["RunLog"] = relationship(back_populates="detection_events")

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<DetectionEventLog(id={self.id}, run_id={self.run_log_id}, image='{self.image_path}')>"
```

---

### `app/models/detection_event.py`

```python
# rpi_counter_fastapi-dev_new/app/models/detection_event.py

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from typing import TYPE_CHECKING # <-- Import TYPE_CHECKING

from .database import Base

# --- THIS IS THE FIX (PART 2) ---
if TYPE_CHECKING:
    from .run_log import RunLog
# --- END OF FIX ---


class QCResult(PyEnum):
    PENDING = "Pending"
    PASS = "Pass"
    FAIL = "Fail"

class DetectionEvent(Base):
    __tablename__ = "detection_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    run_log_id: Mapped[int] = mapped_column(ForeignKey("run_logs.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    
    qc_result: Mapped[QCResult] = mapped_column(Enum(QCResult), default=QCResult.PENDING)
    qc_reason: Mapped[str] = mapped_column(String, nullable=True)

    run_log: Mapped["RunLog"] = relationship(back_populates="detection_events")

    def __repr__(self) -> str:
        return f"<DetectionEvent(id={self.id}, run_log_id={self.run_log_id}, image_path='{self.image_path}')>"
```

---

### `app/models/configuration.py`

```python
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, String, Text, Boolean, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class ConfigDataType(PyEnum):
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    JSON = "json"

class Configuration(Base):
    __tablename__ = "configurations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    namespace: Mapped[str] = mapped_column(String(100), index=True)
    key: Mapped[str] = mapped_column(String(100), index=True)
    value: Mapped[str] = mapped_column(Text)
    data_type: Mapped[ConfigDataType] = mapped_column(Enum(ConfigDataType))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    requires_restart: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    updated_by: Mapped[str] = mapped_column(String(100), default="system")

    def __repr__(self) -> str:
        return f"<Configuration(namespace='{self.namespace}', key='{self.key}')>"

```

---

### `app/models/database.py`

```python
"""
Sets up the asynchronous database engine and session management using SQLAlchemy 2.0.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase
from config import settings

# --- FIX APPLIED HERE ---
# We create a dictionary of engine arguments and conditionally add the
# pooling arguments only if we are NOT using SQLite.
engine_args = {"echo": settings.DATABASE.ECHO}

if "sqlite" not in settings.DATABASE.URL:
    # Add pooling options for databases that support it (e.g., PostgreSQL)
    print("Non-SQLite database detected, applying connection pool settings.")
    engine_args["pool_size"] = settings.DATABASE.POOL_SIZE
    engine_args["pool_timeout"] = settings.DATABASE.POOL_TIMEOUT
else:
    # For SQLite, we add a specific argument to allow it to work with FastAPI
    print("SQLite database detected, omitting pool settings.")
    engine_args["connect_args"] = {"check_same_thread": False}

# Create an async engine instance using the URL from settings
# and the conditionally built arguments.
engine = create_async_engine(
    settings.DATABASE.URL,
    **engine_args
)

# Create a factory for creating new async sessions
AsyncSessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False, # Important for FastAPI dependencies
    class_=AsyncSession
)

class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models. It includes the AsyncAttrs mixin
    to enable async loading of relationships and attributes.
    """
    pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get an async database session per request.
    Ensures the session is always closed, even if errors occur.
    """
    async with AsyncSessionFactory() as session:
        yield session

```

---

### `app/models/operator.py`

```python
from datetime import datetime
from sqlalchemy import Integer, String, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum

from .database import Base

class OperatorStatus(PyEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[OperatorStatus] = mapped_column(Enum(OperatorStatus), default=OperatorStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def __repr__(self) -> str:
        return f"<Operator(id={self.id}, name='{self.name}')>"
```

---

### `app/schemas/operators.py`

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.operator import OperatorStatus


class OperatorBase(BaseModel):
    name: str
    status: OperatorStatus = OperatorStatus.ACTIVE

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[OperatorStatus] = None

class OperatorOut(OperatorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
```

---

### `app/schemas/run_log.py`

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Dict, List # Import List
from datetime import datetime

from .operators import OperatorOut
from .products import ProductOut
from app.models.run_log import RunStatus

# NEW: Pydantic schema for a detection event log
class DetectionEventLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    timestamp: datetime
    image_path: Optional[str] = None

class RunLogBase(BaseModel):
    batch_code: str
    start_timestamp: datetime
    end_timestamp: Optional[datetime] = None
    status: RunStatus
    object_profile_snapshot: Optional[Dict[str, Any]] = None

class RunLogOut(RunLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    operator: Optional[OperatorOut] = None
    product: Optional[ProductOut] = None
    # We can optionally include the events here in the future
    # detection_events: List[DetectionEventLogOut] = []
```

---

### `app/schemas/reports.py`

```python
# rpi_counter_fastapi-dev_new/app/schemas/reports.py

from pydantic import BaseModel
from typing import List, Optional
from .run_log import RunLogOut

class ReportKPIs(BaseModel):
    """Key Performance Indicators for the summary report."""
    total_runs: int
    completed_runs: int
    aborted_runs: int
    failed_runs: int
    success_rate: float # as a percentage
    
class ProductionSummaryReport(BaseModel):
    """The complete payload for the production summary report."""
    kpis: ReportKPIs
    runs: List[RunLogOut]
```

---

### `app/schemas/profiles.py`

```python
"""
NEW: Pydantic schemas for API data validation and serialization
for the CameraProfile and ObjectProfile models.

These schemas define the expected request and response bodies for the
profile management API endpoints.
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from .products import ProductOut

# --- CameraProfile Schemas ---

class CameraProfileBase(BaseModel):
    name: str
    exposure: int = 0
    gain: int = 0
    white_balance_temp: int = 0
    brightness: int = 128
    autofocus: bool = True
    description: Optional[str] = None

class CameraProfileCreate(CameraProfileBase):
    pass

class CameraProfileUpdate(BaseModel):
    # All fields are optional for updates
    name: Optional[str] = None
    exposure: Optional[int] = None
    gain: Optional[int] = None
    white_balance_temp: Optional[int] = None
    brightness: Optional[int] = None
    autofocus: Optional[bool] = None
    
    # This line fixes the 500 Internal Server Error
    description: Optional[str] = None

class CameraProfileOut(CameraProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# --- ObjectProfile Schemas ---

class ObjectProfileBase(BaseModel):
    name: str
    camera_profile_id: int
    sort_offset_ms: int = 0
    description: Optional[str] = None
    product_id: Optional[int] = None

class ObjectProfileCreate(ObjectProfileBase):
    pass

class ObjectProfileUpdate(BaseModel):
    name: Optional[str] = None
    camera_profile_id: Optional[int] = None
    sort_offset_ms: Optional[int] = None
    product_id: Optional[int] = None


class ObjectProfileOut(ObjectProfileBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    camera_profile: CameraProfileOut
    product: Optional[ProductOut] = None
```

---

### `app/schemas/products.py`

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.product import ProductStatus

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    status: ProductStatus = ProductStatus.ACTIVE
    ai_model_path: Optional[str] = "yolov8n.pt"
    min_sensor_block_time_ms: Optional[int] = None
    max_sensor_block_time_ms: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    status: Optional[ProductStatus] = None
    ai_model_path: Optional[str] = None
    min_sensor_block_time_ms: Optional[int] = None
    max_sensor_block_time_ms: Optional[int] = None

class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
```

---

### `app/schemas/detection_event.py`

```python
# rpi_counter_fastapi-dev_new/app/schemas/detection_event.py

from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime
from typing import Optional
import pytz

from app.models.detection_event import QCResult
from config import settings

# --- Timezone Conversion Helper ---
try:
    LOCAL_TZ = pytz.timezone(settings.TIMEZONE)
except pytz.UnknownTimeZoneError:
    LOCAL_TZ = pytz.utc
# ----------------------------------

class DetectionEventBase(BaseModel):
    timestamp: datetime
    image_path: Optional[str] = None
    qc_result: QCResult
    qc_reason: Optional[str] = None

class DetectionEventOut(DetectionEventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    run_log_id: int

    # --- NEW COMPUTED FIELD FOR LOCAL TIME DISPLAY ---
    @computed_field
    @property
    def timestamp_local(self) -> str:
        """Returns a formatted string of the event time in the configured local timezone."""
        if not self.timestamp:
            return ""
        utc_dt = pytz.utc.localize(self.timestamp)
        local_dt = utc_dt.astimezone(LOCAL_TZ)
        return local_dt.strftime('%Y-%m-%d %H:%M:%S')
    # ----------------------------------------------------
```

---

### `scripts/load_test.py`

```python
#!/usr/bin/env python
"""
A simple asynchronous load testing script.
This script bombards an endpoint with concurrent requests to measure performance.
Requires httpx: pip install httpx
"""
import asyncio
import time
import httpx

# --- Configuration ---
BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/v1/system/status" # A lightweight endpoint is good for this
NUM_REQUESTS = 500
CONCURRENCY = 50

async def fetch(client: httpx.AsyncClient):
    """Sends a single GET request."""
    try:
        response = await client.get(f"{BASE_URL}{ENDPOINT}")
        response.raise_for_status()
        return response.status_code
    except httpx.RequestError as e:
        return e

async def run_load_test():
    """Runs the load test with the specified concurrency."""
    print(f"--- Starting Load Test ---")
    print(f"URL: {BASE_URL}{ENDPOINT}")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Concurrency Level: {CONCURRENCY}")
    print("--------------------------")

    async with httpx.AsyncClient() as client:
        semaphore = asyncio.Semaphore(CONCURRENCY)
        
        async def concurrent_fetch():
            async with semaphore:
                return await fetch(client)

        start_time = time.monotonic()
        tasks = [concurrent_fetch() for _ in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)
        end_time = time.monotonic()

    total_time = end_time - start_time
    successful_requests = sum(1 for r in results if isinstance(r, int) and r == 200)
    failed_requests = NUM_REQUESTS - successful_requests
    requests_per_second = successful_requests / total_time if total_time > 0 else 0

    print("\n--- Load Test Results ---")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Requests per second (RPS): {requests_per_second:.2f}")
    print("-------------------------")

if __name__ == "__main__":
    asyncio.run(run_load_test())

```

---

### `scripts/system_test.py`

```python
#!/usr/bin/env python
"""
An end-to-end test script for the Box Counter System.
This script simulates a full workflow by interacting with the running
application's API and WebSocket endpoints.

Requires:
- pip install httpx websockets
- The main application must be running.
- APP_ENV must be set to 'development' for the debug endpoint to be active.
"""
import asyncio
import httpx
import websockets
import json

BASE_URL = "http://localhost:8000"
WEBSOCKET_URL = "ws://localhost:8000/ws"

API_HEADERS = {"Content-Type": "application/json"}
# This should match the API_KEY in your .env file
PROTECTED_API_HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": "your_secret_api_key_here" 
}

async def trigger_sensor(sensor_id: int, state: str):
    """Calls the debug API to simulate a sensor event."""
    async with httpx.AsyncClient() as client:
        print(f"TEST: Triggering Sensor {sensor_id} -> {state}")
        payload = {"sensor_id": sensor_id, "new_state": state}
        try:
            res = await client.post(f"{BASE_URL}/api/v1/debug/sensor-event", json=payload, headers=API_HEADERS)
            res.raise_for_status()
            print(f"  -> API Response: {res.json()}")
        except httpx.RequestError as e:
            print(f"FATAL: Could not trigger sensor. Is the app running in 'development' mode?")
            print(f"  -> {e}")
            exit(1)

async def run_test_sequence():
    """Executes the full end-to-end test sequence."""
    print("--- Starting End-to-End System Test ---")

    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("✓ WebSocket connection established.")

            # 1. Simulate a full box detection cycle
            print("\n--- Simulating Box Detection ---")
            await trigger_sensor(1, "triggered") # Box enters
            await asyncio.sleep(0.2)
            await trigger_sensor(2, "triggered") # Box reaches end
            await asyncio.sleep(0.1)
            await trigger_sensor(1, "cleared")   # Box leaves first sensor (COUNT!)
            await asyncio.sleep(0.2)
            await trigger_sensor(2, "cleared")   # Box fully exits
            
            # 2. Listen on WebSocket for count update
            print("\n--- Waiting for WebSocket update... ---")
            count_updated = False
            try:
                async for message in websocket:
                    data = json.loads(message)
                    if data.get("type") == "detection_status" and data["data"]["count"] >= 1:
                        print(f"✓ SUCCESS: WebSocket reported new count: {data['data']['count']}")
                        count_updated = True
                        break # Exit the listener loop
                    # Timeout to prevent infinite loop
                    # This is a simplified listener for the test
                    await asyncio.sleep(0.1) # Yield control
            except asyncio.TimeoutError:
                print("✗ FAILURE: Timed out waiting for WebSocket count update.")

            if not count_updated:
                # If the specific message wasn't received after a short while
                print("✗ FAILURE: Did not receive expected WebSocket message.")

            # 3. Reset the counter via API
            print("\n--- Testing Counter Reset API ---")
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{BASE_URL}/api/v1/detection/reset", headers=API_HEADERS)
                if res.status_code == 200:
                    print(f"✓ SUCCESS: Reset API returned OK.")
                else:
                    print(f"✗ FAILURE: Reset API failed with status {res.status_code}")

            # 4. Test a protected endpoint (Emergency Stop)
            print("\n--- Testing Protected API Endpoint (Emergency Stop) ---")
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{BASE_URL}/api/v1/system/emergency-stop", headers=PROTECTED_API_HEADERS)
                if res.status_code == 200:
                    print(f"✓ SUCCESS: Protected endpoint returned OK.")
                else:
                    print(f"✗ FAILURE: Protected endpoint failed with status {res.status_code}. Check your API Key.")

    except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError) as e:
        print("\n✗ FATAL: Could not connect to the application.")
        print("Please ensure the FastAPI server is running before executing this test.")
        return

    print("\n--- End-to-End System Test Finished ---")

if __name__ == "__main__":
    asyncio.run(run_test_sequence())

```

---

### `scripts/benchmark.py`

```python
#!/usr/bin/env python
"""
A simple asynchronous benchmarking script to test API endpoint performance.
Requires httpx: pip install httpx
"""
import asyncio
import time
import httpx

# --- Configuration ---
BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/v1/system/status"
NUM_REQUESTS = 200
CONCURRENCY = 20

async def fetch(client: httpx.AsyncClient):
    """Sends a single GET request."""
    try:
        response = await client.get(f"{BASE_URL}{ENDPOINT}")
        response.raise_for_status()
        return response.status_code
    except httpx.RequestError as e:
        print(f"An error occurred: {e}")
        return None

async def run_benchmark():
    """Runs the benchmark with the specified concurrency."""
    print(f"--- Starting Benchmark ---")
    print(f"URL: {BASE_URL}{ENDPOINT}")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Concurrency Level: {CONCURRENCY}")
    print("--------------------------")

    async with httpx.AsyncClient() as client:
        semaphore = asyncio.Semaphore(CONCURRENCY)
        
        async def concurrent_fetch():
            async with semaphore:
                return await fetch(client)

        start_time = time.monotonic()
        tasks = [concurrent_fetch() for _ in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)
        end_time = time.monotonic()

    total_time = end_time - start_time
    successful_requests = sum(1 for r in results if r == 200)
    failed_requests = NUM_REQUESTS - successful_requests
    requests_per_second = successful_requests / total_time if total_time > 0 else 0

    print("\n--- Benchmark Results ---")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Requests per second (RPS): {requests_per_second:.2f}")
    print("-------------------------")

if __name__ == "__main__":
    asyncio.run(run_benchmark())

```

---

### `config/__init__.py`

```python
"""
This file initializes the settings for the main application and derives
the list of active cameras, providing a single source of truth.
"""
from .settings import get_settings

# Create the global settings object for the main app
settings = get_settings()

# Derive the list of active camera IDs from the loaded settings
ACTIVE_CAMERA_IDS = []
# The CAMERA_MODE is read from the .env file by the AppSettings class
if settings.CAMERA_MODE in ['rpi', 'both']:
    ACTIVE_CAMERA_IDS.append('rpi')
if settings.CAMERA_MODE in ['usb', 'both']:
    ACTIVE_CAMERA_IDS.append('usb')

print(f"[Main App Config] Mode: '{settings.CAMERA_MODE}'. Active cameras: {ACTIVE_CAMERA_IDS}")
```

---

### `config/settings.py`

```python
from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Nested Settings Classes ---

class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SERVER_', case_sensitive=False)
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = Field(..., min_length=32)

class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SECURITY_', case_sensitive=False)
    API_KEY: str

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_', case_sensitive=False)
    URL: str = "sqlite+aiosqlite:///./data/box_counter.db"
    ECHO: bool = False

class BaseCameraSettings(BaseSettings):
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)

class RpiCameraSettings(BaseCameraSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_RPI_', case_sensitive=False)
    ID: str = ""
    SHUTTER_SPEED: int = Field(0, ge=0)
    ISO: int = Field(0, ge=0)
    MANUAL_FOCUS: float = Field(0.0, ge=0.0)

class UsbCameraSettings(BaseCameraSettings):
    model_config = SettingsConfigDict(env_prefix='CAMERA_USB_', case_sensitive=False)
    DEVICE_INDEX: int = 0
    EXPOSURE: int = 0
    GAIN: int = 0
    BRIGHTNESS: int = Field(128, ge=0, le=255)
    AUTOFOCUS: bool = True
    WHITE_BALANCE_TEMP: int = 0

class OutputChannelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='OUTPUTS_', case_sensitive=False)
    CONVEYOR: int = 0
    GATE: int = 1
    DIVERTER: int = 2
    LED_GREEN: int = 3
    LED_RED: int = 4
    CAMERA_LIGHT: int = 5
    BUZZER: int = 6

class ModbusSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MODBUS_', case_sensitive=False)
    PORT: str = "/dev/ttyUSB0"
    BAUDRATE: int = 9600
    DEVICE_ADDRESS_INPUTS: int = 1
    DEVICE_ADDRESS_OUTPUTS: int = 2
    TIMEOUT_SEC: float = 0.5
    POLLING_MS: int = 50

class SensorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SENSORS_', case_sensitive=False)
    ENTRY_CHANNEL: int = 1
    EXIT_CHANNEL: int = 3

class OrchestrationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='ORCHESTRATION_', case_sensitive=False)
    POST_BATCH_DELAY_SEC: int = 5

class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LOGGING_', case_sensitive=False)
    VERBOSE_LOGGING: bool = False

# --- NEW: Settings for timed buzzer alerts ---
class BuzzerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BUZZER_', case_sensitive=False)
    MISMATCH_MS: int = Field(500, description="Buzzer duration in ms for a product size mismatch.")
    MANUAL_TOGGLE_MS: int = Field(200, description="Buzzer duration in ms for a manual toggle from the UI.")
    LOOP_COMPLETE_MS: int = Field(1000, description="Buzzer duration in ms when a batch loop completes.")
    EXIT_SENSOR_MS: int = Field(150, description="Buzzer duration in ms when the exit sensor is triggered.")

class ConveyorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CONVEYOR_', case_sensitive=False)
    SPEED_M_PER_SEC: float = 0.5
    CAMERA_TO_SORTER_DISTANCE_M: float = 1.0
    # --- NEW: Setting for the post-run stop delay ---
    CONVEYOR_AUTO_STOP_DELAY_SEC: int = Field(2, description="How many seconds the conveyor runs after the last box of a batch is counted before stopping.")
    MAX_TRANSIT_TIME_SEC: float = Field(15.0, gt=0, description="Max time for a product to travel from entry to exit before a failure is triggered.")


# --- Main AppSettings Container ---

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)

    PROJECT_NAME: str = "Raspberry Pi 5 Box Counter System"
    PROJECT_VERSION: str = "10.0.0-No-AI"
    APP_ENV: Literal["development", "production"] = "development"
    CAMERA_MODE: Literal['rpi', 'usb', 'both', 'none'] = 'both'
    CAMERA_TRIGGER_DELAY_MS: int = 100
    CAMERA_CAPTURES_DIR: str = "web/static/captures"
    UI_ANIMATION_TRANSIT_TIME_SEC: int = Field(5, gt=0)


    # Nested configuration objects
    CAMERA_RPI: RpiCameraSettings = RpiCameraSettings()
    CAMERA_USB: UsbCameraSettings = UsbCameraSettings()
    SERVER: ServerSettings = ServerSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    DATABASE: DatabaseSettings = DatabaseSettings()
    OUTPUTS: OutputChannelSettings = OutputChannelSettings()
    MODBUS: ModbusSettings = ModbusSettings()
    SENSORS: SensorSettings = SensorSettings()
    ORCHESTRATION: OrchestrationSettings = OrchestrationSettings()
    LOGGING: LoggingSettings = LoggingSettings()
    CONVEYOR: ConveyorSettings = ConveyorSettings()
    # --- NEW: Add the buzzer settings to the main config ---
    BUZZER: BuzzerSettings = BuzzerSettings()

@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
```

---

### `services/camera_service_rpi.py`

```python
"""
Standalone Camera Service for the Raspberry Pi Camera Module.
FINAL REVISION: This script is now completely self-contained and robust.

- It now checks if the connected camera supports autofocus before attempting
  to set autofocus controls, fixing the AttributeError for fixed-focus cameras
  like the imx219. This makes the script compatible with multiple camera models.
- It correctly finds the numerical index of the camera based on the ID string.
- It continues to listen to the Redis command channel for on-the-fly profile updates.
"""
import time
import cv2
import redis
import traceback
import json
import threading
from pathlib import Path
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Global Camera Object ---
camera = None

# --- Robust Path and Configuration ---
ENV_PATH = Path(__file__).parent.parent / ".env"

class RpiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_prefix='CAMERA_RPI_', case_sensitive=False, extra='ignore')
    ID: str
    RESOLUTION_WIDTH: int = 1280
    RESOLUTION_HEIGHT: int = 720
    FPS: int = 30
    JPEG_QUALITY: int = Field(90, ge=10, le=100)

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_prefix='REDIS_', case_sensitive=False, extra='ignore')
    HOST: str = 'localhost'
    PORT: int = 6379

REDIS_COMMAND_CHANNEL = "camera:commands:rpi"

def apply_camera_settings(settings_dict: dict):
    """Applies a dictionary of settings to the global picamera2 object."""
    global camera
    if camera is None:
        print("[RPI Camera Service] Error: Cannot apply settings, camera is not available.", flush=True)
        return

    print("\n--- Applying New RPi Camera Settings from Command ---", flush=True)
    from picamera2 import controls
    
    controls_to_set = {}
    
    # --- DEFINITIVE FIX: Check if the camera supports Autofocus before setting it ---
    if 'autofocus' in settings_dict:
        # Check the list of available controls for this specific camera model.
        if 'AfMode' in camera.camera_controls:
            af_mode = controls.AfMode.Continuous if settings_dict['autofocus'] else controls.AfMode.Manual
            controls_to_set['AfMode'] = af_mode
            print(f"  -> AF Mode: {af_mode.name}", flush=True)
        else:
            # If the control doesn't exist, inform the user and skip it.
            print("  -> AF Mode: Not supported by this camera model (imx219). Skipping.", flush=True)

    if 'white_balance_temp' in settings_dict:
        controls_to_set['AwbEnable'] = settings_dict['white_balance_temp'] == 0
        print(f"  -> AWB Enable: {controls_to_set['AwbEnable']}", flush=True)
    
    use_auto_exposure = True
    if 'gain' in settings_dict and settings_dict['gain'] > 0:
        controls_to_set['AnalogueGain'] = float(settings_dict['gain'])
        use_auto_exposure = False
        print(f"  -> Manual AnalogueGain: {controls_to_set['AnalogueGain']}", flush=True)
        
    if 'exposure' in settings_dict and settings_dict['exposure'] > 0:
        controls_to_set['ExposureTime'] = settings_dict['exposure']
        use_auto_exposure = False
        print(f"  -> Manual ExposureTime (µs): {controls_to_set['ExposureTime']}", flush=True)

    controls_to_set['AeEnable'] = use_auto_exposure
    print(f"  -> Auto Exposure Enable: {use_auto_exposure}", flush=True)

    if 'brightness' in settings_dict:
        scaled_brightness = (settings_dict['brightness'] / 255.0) * 2.0 - 1.0
        controls_to_set['Brightness'] = scaled_brightness
        print(f"  -> Brightness: {scaled_brightness:.2f}", flush=True)

    if controls_to_set:
        camera.set_controls(controls_to_set)
    print("-------------------------------------------\n", flush=True)

def command_listener(redis_client: redis.Redis):
    """A thread that listens for commands and applies settings."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_COMMAND_CHANNEL)
    print(f"[Command Listener] Subscribed to '{REDIS_COMMAND_CHANNEL}' for live commands.", flush=True)
    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                command = json.loads(message['data'])
                if command.get('action') == 'apply_settings':
                    settings_to_apply = command.get('settings')
                    if isinstance(settings_to_apply, dict):
                        apply_camera_settings(settings_to_apply)
            except Exception as e:
                print(f"[Command Listener] Error processing command: {e}", flush=True)

def main():
    global camera
    try:
        rpi_cam_settings = RpiSettings()
        redis_settings = RedisSettings()
    except ValidationError as e:
        if any(err.get('type') == 'missing' and err.get('loc') == ('ID',) for err in e.errors()):
            print("\n" + "="*60, "\n--- CONFIGURATION ERROR ---")
            print("FATAL: The 'CAMERA_RPI_ID' is missing from your .env file.")
            print("\nTo fix this: run 'libcamera-hello --list-cameras', copy the ID,")
            print(f"and add it to your .env file at: {ENV_PATH}")
            print("\n   CAMERA_RPI_ID='your_camera_id_here'\n" + "="*60 + "\n")
            return
        else:
            raise

    redis_client = None
    try:
        from picamera2 import Picamera2
        
        target_camera_id = rpi_cam_settings.ID
        all_cameras_info = Picamera2.global_camera_info()
        if not all_cameras_info:
            print("FATAL ERROR: No cameras found by the libcamera system. Check hardware connection.")
            return

        camera_index = None
        for i, info in enumerate(all_cameras_info):
            if info['Id'] == target_camera_id:
                camera_index = i
                break
        
        if camera_index is None:
            print("\n" + "="*70, "\n--- CAMERA NOT FOUND ERROR ---")
            print(f"FATAL: The camera ID '{target_camera_id}' from your .env file was NOT FOUND.")
            print("\nAvailable cameras are:")
            for i, info in enumerate(all_cameras_info):
                print(f"  - Index {i}: {info['Id']} ({info['Model']})")
            print("\nPlease ensure the correct ID is copied into your .env file.", "\n" + "="*70 + "\n")
            return
        
        redis_client = redis.Redis(host=redis_settings.HOST, port=redis_settings.PORT, decode_responses=True)
        redis_client.ping()
        print("[RPI Camera Service] Redis connection successful.", flush=True)

        listener_thread = threading.Thread(target=command_listener, args=(redis_client,), daemon=True)
        listener_thread.start()

        print(f"[RPI Camera Service] Initializing camera at index {camera_index} (ID: {target_camera_id})", flush=True)
        camera = Picamera2(camera_index)
        
        config = camera.create_video_configuration(
            main={"size": (rpi_cam_settings.RESOLUTION_WIDTH, rpi_cam_settings.RESOLUTION_HEIGHT), "format": "RGB888"}
        )
        camera.configure(config)
        camera.set_controls({"FrameRate": rpi_cam_settings.FPS})
        
        # This will now run without crashing, as it will intelligently skip the
        # unsupported autofocus setting.
        apply_camera_settings({'autofocus': True, 'white_balance_temp': 0})
        
        camera.start()
        frame_channel = 'camera:frames:rpi'
        print(f"[RPI Camera Service] Camera started. Publishing to '{frame_channel}'.", flush=True)
        time.sleep(2) 

        while True:
            frame = camera.capture_array()
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, rpi_cam_settings.JPEG_QUALITY])
            redis_client.publish(frame_channel, buffer.tobytes())

    except ImportError:
        print("[RPI Camera Service] FATAL ERROR: The 'picamera2' library is not installed.", flush=True)
    except Exception as e:
        print(f"[RPI Camera Service] FATAL ERROR: An unexpected error occurred.", flush=True)
        print(traceback.format_exc(), flush=True)
    finally:
        if 'camera' in locals() and camera and camera.is_open:
            camera.stop()
        if 'redis_client' in locals() and redis_client:
            redis_client.close()
        print("[RPI Camera Service] Exited.", flush=True)

if __name__ == "__main__":
    main()
```

---

### `services/camera_service_usb.py`

```python
"""
Standalone Camera Service for a USB V4L2 Camera.
FINAL ARCHITECTURE: This service is now a 'dumb' command receiver.

- It NO LONGER reads camera profiles (exposure, gain, etc.) from any file.
- It loads only essential hardware constants (device index, jpeg quality) from .env.
- It starts up with simple 'auto' settings.
- It listens on a Redis channel for commands from the main application, which
  will tell it which settings to apply on the fly.
- ADDED: Verbose logging to diagnose frame publishing issues.
"""
import time
import cv2
import redis
import traceback
import json
import threading
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Constants and Paths ---
ENV_PATH = Path(__file__).parent.parent / ".env"
REDIS_COMMAND_CHANNEL = "camera:commands:usb"
camera = None # Global camera object

# --- Simple Settings Loader for Essential Hardware Config ONLY ---
class UsbHardwareSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='CAMERA_USB_',
        case_sensitive=False,
        env_file=str(ENV_PATH),
        extra='ignore'
    )
    DEVICE_INDEX: int = 0
    JPEG_QUALITY: int = 90

def apply_camera_settings(settings_dict: dict):
    """Applies a dictionary of settings to the global camera object."""
    global camera
    if camera is None or not camera.isOpened():
        print("[USB Camera Service] Error: Cannot apply settings, camera is not available.", flush=True)
        return

    print("\n--- Applying New Camera Settings from Command ---", flush=True)
    
    autofocus = settings_dict.get('autofocus', True)
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 1 if autofocus else 0)
    print(f"  -> Autofocus: {'On' if autofocus else 'Off'}", flush=True)
    
    wb_temp = settings_dict.get('white_balance_temp', 0)
    if wb_temp > 0:
        camera.set(cv2.CAP_PROP_AUTO_WB, 0)
        camera.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, wb_temp)
        print(f"  -> Manual White Balance: {wb_temp}", flush=True)
    else:
        camera.set(cv2.CAP_PROP_AUTO_WB, 1)
        print(f"  -> Auto White Balance", flush=True)
        
    gain = settings_dict.get('gain', 0)
    if gain >= 0: # Gain can be 0
        camera.set(cv2.CAP_PROP_GAIN, gain)
        print(f"  -> Manual Gain: {gain}", flush=True)
    
    brightness = settings_dict.get('brightness', 128)
    camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    print(f"  -> Brightness: {brightness}", flush=True)

    exposure = settings_dict.get('exposure', 0)
    if exposure != 0:
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        camera.set(cv2.CAP_PROP_EXPOSURE, exposure)
        print(f"  -> Manual Exposure: {exposure}", flush=True)
    else:
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        print(f"  -> Auto Exposure", flush=True)
    print("-------------------------------------------\n", flush=True)


def command_listener(redis_client: redis.Redis):
    """A thread that listens for commands and applies settings."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_COMMAND_CHANNEL)
    print(f"[Command Listener] Subscribed to '{REDIS_COMMAND_CHANNEL}' for live commands.", flush=True)
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                command = json.loads(message['data'])
                if command.get('action') == 'apply_settings':
                    settings_to_apply = command.get('settings')
                    if isinstance(settings_to_apply, dict):
                        apply_camera_settings(settings_to_apply)
            except Exception as e:
                print(f"[Command Listener] Error processing command: {e}", flush=True)

def main():
    global camera
    hardware_settings = UsbHardwareSettings()
    redis_client = None

    try:
        redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        redis_client.ping()
        print("[USB Camera Service] Redis connection successful.", flush=True)

        listener_thread = threading.Thread(target=command_listener, args=(redis_client,), daemon=True)
        listener_thread.start()

        print(f"[USB Camera Service] Opening camera at index {hardware_settings.DEVICE_INDEX}...", flush=True)
        camera = cv2.VideoCapture(hardware_settings.DEVICE_INDEX, cv2.CAP_V4L2)
        if not camera.isOpened():
            raise RuntimeError(f"Could not open camera at index {hardware_settings.DEVICE_INDEX}.")
        print("[USB Camera Service] Camera opened successfully.", flush=True)

        apply_camera_settings({})
        
        frame_channel = 'camera:frames:usb'
        print(f"[USB Camera Service] Starting capture loop. Publishing to '{frame_channel}'.", flush=True)
        time.sleep(1)

        frame_count = 0
        last_log_time = time.time()
        while True:
            ret, frame = camera.read()
            if not ret:
                print("[USB Camera Service] WARNING: camera.read() returned False. Check camera connection.", flush=True)
                time.sleep(1) 
                continue

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, hardware_settings.JPEG_QUALITY])
            redis_client.publish(frame_channel, buffer.tobytes())
            frame_count += 1
            
            # Log status every 5 seconds
            current_time = time.time()
            if current_time - last_log_time >= 5.0:
                print(f"[USB Camera Service] Published {frame_count} frames to '{frame_channel}' in the last 5 seconds.", flush=True)
                frame_count = 0
                last_log_time = current_time


    except Exception as e:
        print(f"[USB Camera Service] FATAL ERROR: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
    finally:
        if camera and camera.isOpened(): camera.release()
        if redis_client: redis_client.close()
        print("[USB Camera Service] Exited.", flush=True)

if __name__ == "__main__":
    main()
```

---

### `tests/test_api.py`

```python
"""
Tests for the FastAPI API endpoints.
"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Tests the main health check/root endpoint."""
    response = await async_client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_usage" in data
    assert "camera_status" in data
    assert data["camera_status"] == "connected" # From our mock

@pytest.mark.asyncio
async def test_get_detection_status(async_client: AsyncClient):
    """Tests the initial state of the detection endpoint."""
    response = await async_client.get("/api/v1/detection/")
    assert response.status_code == 200
    data = response.json()
    assert data["box_count"] == 0
    assert data["state"] == "IDLE"

@pytest.mark.asyncio
async def test_reset_counter(async_client: AsyncClient):
    """Tests the counter reset functionality."""
    # This is a simple test; a more complex one would simulate a count first.
    response = await async_client.post("/api/v1/detection/reset")
    assert response.status_code == 200
    assert response.json() == {"message": "Counter reset successfully."}
    
    # Verify the count is still 0
    response = await async_client.get("/api/v1/detection/")
    assert response.status_code == 200
    assert response.json()["box_count"] == 0

@pytest.mark.asyncio
async def test_conveyor_control(async_client: AsyncClient):
    """Tests starting and stopping the mock conveyor."""
    # Start the conveyor
    start_response = await async_client.post("/api/v1/gpio/conveyor/start")
    assert start_response.status_code == 200
    assert start_response.json()["message"] == "Conveyor started."

    # Check status
    status_response = await async_client.get("/api/v1/gpio/status")
    assert status_response.json()["conveyor"] == "running"

    # Stop the conveyor
    stop_response = await async_client.post("/api/v1/gpio/conveyor/stop")
    assert stop_response.status_code == 200
    assert stop_response.json()["message"] == "Conveyor stopped."
    
    # Check status again
    status_response = await async_client.get("/api/v1/gpio/status")
    assert status_response.json()["conveyor"] == "stopped"

```

---

### `tests/conftest.py`

```python
"""
Pytest configuration file for defining shared fixtures.
"""
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Import all necessary components
from main import create_app
from config import settings # FIX: Import the application settings
from app.models.database import Base, get_async_session
from app.core.gpio_controller import AsyncGPIOController
from app.services.detection_service import AsyncDetectionService

# --- Database Setup for Tests ---
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
TestAsyncSessionFactory = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

# --- Auto-use Fixture to Manage Schema ---
@pytest_asyncio.fixture(scope="function", autouse=True)
async def db_schema() -> AsyncGenerator[None, None]:
    """Auto-used fixture to create and drop the database schema for every test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --- Session Fixture ---
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a single database session for tests that need it directly."""
    async with TestAsyncSessionFactory() as session:
        yield session

# --- API Test Client Fixture ---
@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provides an async test client that correctly handles the application lifespan."""
    app = create_app()
    app.dependency_overrides[get_async_session] = lambda: db_session
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client

# --- DEFINITIVE FIX: Service Fixture ---
@pytest_asyncio.fixture(scope="function")
async def detection_service(db_session: AsyncSession) -> AsyncDetectionService:
    """
    Provides a fully initialized instance of the AsyncDetectionService
    connected to the clean test database.
    """
    gpio_controller = await AsyncGPIOController.get_instance()
    
    # FIX: The required 'sensor_config' argument is now provided.
    service = AsyncDetectionService(
        gpio_controller=gpio_controller,
        db_session_factory=TestAsyncSessionFactory,
        sensor_config=settings.SENSORS 
    )
    
    # Initialize the service, which will load its state from the (empty) DB.
    await service.initialize()
    return service
```

---

### `tests/test_models.py`

```python
"""
Tests for the SQLAlchemy database models.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# FIX APPLIED HERE: Import Detection and DetectionDirection from their specific module.
from app.models.detection import Detection, DetectionDirection

@pytest.mark.asyncio
async def test_create_detection_record(db_session: AsyncSession):
    """
    Tests the creation and retrieval of a Detection model instance.
    """
    # Create a new detection record
    new_detection = Detection(
        box_count=1,
        detection_direction=DetectionDirection.FORWARD,
        confidence_score=0.95
    )
    db_session.add(new_detection)
    await db_session.commit()
    await db_session.refresh(new_detection)

    # Retrieve it from the database
    result = await db_session.execute(select(Detection).where(Detection.id == new_detection.id))
    retrieved_detection = result.scalar_one()

    assert retrieved_detection is not None
    assert retrieved_detection.id == new_detection.id
    assert retrieved_detection.box_count == 1
    assert retrieved_detection.confidence_score == 0.95
    assert retrieved_detection.detection_direction == DetectionDirection.FORWARD

```

---

### `tests/test_services.py`

```python
"""
Tests for the business logic services.
"""
import pytest
import asyncio

from app.core.sensor_events import SensorEvent, SensorState
from app.services.detection_service import AsyncDetectionService, DetectionState

@pytest.mark.asyncio
async def test_detection_service_state_machine(detection_service: AsyncDetectionService):
    """
    Tests the full state machine logic using a pre-initialized service from a fixture.
    This pattern is robust and ensures the database is correctly set up.
    """
    # The `detection_service` is provided by the fixture in conftest.py,
    # fully initialized and connected to a clean test database.

    assert detection_service._state == DetectionState.IDLE
    assert await detection_service.get_current_count() == 0

    # 1. Box enters - trigger sensor 1
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=1, new_state=SensorState.TRIGGERED))
    assert detection_service._state == DetectionState.ENTERING

    # 2. Box hits second sensor
    await asyncio.sleep(0.2)
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=2, new_state=SensorState.TRIGGERED))
    assert detection_service._state == DetectionState.CONFIRMING_EXIT

    # 3. Box clears first sensor - THIS IS THE COUNTING EVENT
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=1, new_state=SensorState.CLEARED))
    assert detection_service._state == DetectionState.RESETTING
    assert await detection_service.get_current_count() == 1

    # 4. Box fully clears second sensor
    await detection_service.handle_sensor_event(SensorEvent(sensor_id=2, new_state=SensorState.CLEARED))
    assert detection_service._state == DetectionState.IDLE

```
