# Starter Kit using Python in Flask framework

## Server Setup
* Install Python 3.10
* Create and activate Virtual Environment
* Install requirements
```commandline
pip install -r requirements.txt
```
* Migrate Database
```commandline
flask db init
flask db migrate
flask db upgrade
```
* Run Server
```commandline
flask run
```

## Tests
Pytest (python package) is being used in the tests. All test files
should be in the tests directory and file name should start with test_


For Example

```doctest
test_module.py
```
And all test function should also start with test_

For Example.
```doctest
def test_get_records():
    records = Records.get_all()
    assert len(records) == 2
```
We have two types of tests in this starter kit.
* Integration tests (To test the APIs)
* Unit tests (To test each an every function)

You can run the tests with the following commands.
* Run all tests.
```commandline
pytest
```
* Run tests in a directory
```commandline
pytest tests/
```
* Run a specific file.
```commandline
pytest tests/filename.py
```
* Run a test a specific file
```commandline
pytest tests/filename.py::test_method
```
* Run a test class from a specific file
```commandline
pytest tests/filename.py::TestClass
```
* Run a test of a test class from a specific file
```commandline
pytest tests/filename.py::TestClass::test_method
```
Output of pytest:
```doctest
PS C:\Users\PuneetDixit\Desktop\starter-kit> pytest

=============================================================== test session starts ===============================================================
platform win32 -- Python 3.10.9, pytest-7.3.0, pluggy-1.0.0
rootdir: C:\Users\PuneetDixit\Desktop\user-login
configfile: pytest.ini
plugins: cov-4.0.0, mock-3.10.0
collected 73 items

tests\integration_tests\test_address.py .......                                                                                             [ 7/73]
tests\integration_tests\test_auth.py ..........                                                                                             [17/73]
tests\integration_tests\test_user.py .....                                                                                                  [22/73]
tests\unit_tests\modules\address\test_address_controller.py ....                                                                            [26/73]
tests\unit_tests\modules\address\test_address_model.py ..                                                                                   [28/73]
tests\unit_tests\modules\address\test_address_schema_validator.py ..                                                                        [30/73]
tests\unit_tests\modules\address\test_address_view.py .....                                                                                 [35/73]
tests\unit_tests\modules\auth\test_auth_controller.py ......                                                                                [41/73]
tests\unit_tests\modules\auth\test_auth_model.py ....                                                                                       [45/73]
tests\unit_tests\modules\auth\test_auth_schema_validator.py ...                                                                             [48/73]
tests\unit_tests\modules\auth\test_auth_view.py .....                                                                                       [53/73]
tests\unit_tests\modules\user\test_user_controller.py ...                                                                                   [56/73]
tests\unit_tests\modules\user\test_user_model.py .                                                                                          [57/73]
tests\unit_tests\modules\user\test_user_schema_validator.py .                                                                               [58/73]
tests\unit_tests\modules\user\test_user_view.py .....                                                                                       [63/73]
tests\unit_tests\others\test_custom_exceptions.py ....                                                                                      [67/73]
tests\unit_tests\others\test_init_file.py .                                                                                                 [68/73]
tests\unit_tests\others\test_logger.py ..                                                                                                   [70/73]
tests\unit_tests\others\test_utils.py ...                                                                                                   [73/73]

=============================================================== 73 passed in 22.36s ===============================================================
```
## Code Coverage by tests
To check the code coverage by tests we are using
coverage package. We can check the coverage (how
much tests is covered by unit and integration tests)
by tests of each directory.

You can check the coverage of unit tests and integration_tests separately

Command to run the coverage.
```commandline
coverage run --source=main -m pytest -v ./tests ; coverage report -m
```
Output of coverage:
```doctest
PS C:\Users\PuneetDixit\Desktop\starter-kit> coverage run --source=main -m pytest -v ./tests ; coverage report -m

=============================================================== test session starts ===============================================================
platform win32 -- Python 3.10.9, pytest-7.3.0, pluggy-1.0.0 -- C:\Users\PuneetDixit\Desktop\Starter App\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\PuneetDixit\Desktop\user-login
configfile: pytest.ini
plugins: cov-4.0.0, mock-3.10.0
collected 73 items

tests/integration_tests/test_address.py::test_add_address PASSED                                                                            [ 1/73]
tests/integration_tests/test_address.py::test_get_addresses PASSED                                                                          [ 2/73]
tests/integration_tests/test_address.py::test_get_address_by_id PASSED                                                                      [ 3/73]
tests/integration_tests/test_address.py::test_update_address PASSED                                                                         [ 4/73]
tests/integration_tests/test_address.py::test_delete_address PASSED                                                                         [ 5/73]
tests/integration_tests/test_address.py::test_get_addresses_using_admin PASSED                                                              [ 6/73]
tests/integration_tests/test_address.py::test_unauthorized_user_error PASSED                                                                [ 7/73]
tests/integration_tests/test_auth.py::test_login_success PASSED                                                                             [ 8/73]
tests/integration_tests/test_auth.py::test_login_failure PASSED                                                                             [ 9/73]
tests/integration_tests/test_auth.py::test_update_password PASSED                                                                           [10/73]
tests/integration_tests/test_auth.py::test_failure_update_password PASSED                                                                   [11/73]
tests/integration_tests/test_auth.py::test_signup_success PASSED                                                                            [12/73]
tests/integration_tests/test_auth.py::test_signup_failure_minimum_password_length PASSED                                                    [13/73]
tests/integration_tests/test_auth.py::test_signup_user_already_exists PASSED                                                                [14/73]
tests/integration_tests/test_auth.py::test_login_failure_with_wrong_email PASSED                                                            [15/73]
tests/integration_tests/test_auth.py::test_get_access_token_using_refresh_token PASSED                                                      [16/73]
tests/integration_tests/test_auth.py::test_logout PASSED                                                                                    [17/73]
tests/integration_tests/test_user.py::test_get_user_profile PASSED                                                                          [18/73]
tests/integration_tests/test_user.py::test_update_user_profile PASSED                                                                       [19/73]
tests/integration_tests/test_user.py::test_get_all_users_profiles PASSED                                                                    [20/73]
tests/integration_tests/test_user.py::test_get_users_profile_by_id PASSED                                                                   [21/73]
tests/integration_tests/test_user.py::test_update_users_profile_by_id PASSED                                                                [22/73]
tests/unit_tests/modules/address/test_address_controller.py::test_delete_address PASSED                                                     [23/73]
tests/unit_tests/modules/address/test_address_controller.py::test_create_new_address PASSED                                                 [24/73]
tests/unit_tests/modules/address/test_address_controller.py::test_get_address PASSED                                                        [25/73]
tests/unit_tests/modules/address/test_address_controller.py::test_update_address PASSED                                                     [26/73]
tests/unit_tests/modules/address/test_address_model.py::test_get_all_address PASSED                                                         [27/73]
tests/unit_tests/modules/address/test_address_model.py::test_add_address PASSED                                                             [28/73]
tests/unit_tests/modules/address/test_address_schema_validator.py::TestAddressSchemaValidators::test_add_address_schema PASSED              [29/73]
tests/unit_tests/modules/address/test_address_schema_validator.py::TestAddressSchemaValidators::test_update_address_schema PASSED           [30/73]
tests/unit_tests/modules/address/test_address_view.py::TestAddressApi::test_get PASSED                                                      [31/73]
tests/unit_tests/modules/address/test_address_view.py::TestAddressApi::test_post PASSED                                                     [32/73]
tests/unit_tests/modules/address/test_address_view.py::TestAddressApi2::test_get PASSED                                                     [33/73]
tests/unit_tests/modules/address/test_address_view.py::TestAddressApi2::test_put PASSED                                                     [34/73]
tests/unit_tests/modules/address/test_address_view.py::TestAddressApi2::test_delete PASSED                                                  [35/73]
tests/unit_tests/modules/auth/test_auth_controller.py::test_create_new_user PASSED                                                          [36/73]
tests/unit_tests/modules/auth/test_auth_controller.py::test_get_current_user PASSED                                                         [37/73]
tests/unit_tests/modules/auth/test_auth_controller.py::test_update_user_password PASSED                                                     [38/73]
tests/unit_tests/modules/auth/test_auth_controller.py::test_get_token PASSED                                                                [39/73]
tests/unit_tests/modules/auth/test_auth_controller.py::test_get_access_token_from_refresh_token PASSED                                      [40/73]
tests/unit_tests/modules/auth/test_auth_controller.py::test_logout PASSED                                                                   [41/73]
tests/unit_tests/modules/auth/test_auth_model.py::TestAuthModel::test_get_all_users PASSED                                                  [42/73]
tests/unit_tests/modules/auth/test_auth_model.py::TestAuthModel::test_create_user PASSED                                                    [43/73]
tests/unit_tests/modules/auth/test_auth_model.py::TestAuthModel::test_update_user PASSED                                                    [44/73]
tests/unit_tests/modules/auth/test_auth_model.py::TestAuthModel::test_delete_user PASSED                                                    [45/73]
tests/unit_tests/modules/auth/test_auth_schema_validator.py::TestAuthSchemaValidators::test_sign_up_schema PASSED                           [46/73]
tests/unit_tests/modules/auth/test_auth_schema_validator.py::TestAuthSchemaValidators::test_log_in_schema PASSED                            [47/73]
tests/unit_tests/modules/auth/test_auth_schema_validator.py::TestAuthSchemaValidators::test_update_password_schema PASSED                   [48/73]
tests/unit_tests/modules/auth/test_auth_view.py::TestSignUpApi::test_post PASSED                                                            [49/73]
tests/unit_tests/modules/auth/test_auth_view.py::TestLoginApi::test_post PASSED                                                             [50/73]
tests/unit_tests/modules/auth/test_auth_view.py::TestRefresh::test_get PASSED                                                               [51/73]
tests/unit_tests/modules/auth/test_auth_view.py::TestChangePassword::test_put PASSED                                                        [52/73]
tests/unit_tests/modules/auth/test_auth_view.py::TestLogout::test_delete PASSED                                                             [53/73]
tests/unit_tests/modules/user/test_user_controller.py::test_get_user_profile PASSED                                                         [54/73]
tests/unit_tests/modules/user/test_user_controller.py::test_update_user_profile PASSED                                                      [55/73]
tests/unit_tests/modules/user/test_user_controller.py::test_get_users_profile PASSED                                                        [56/73]
tests/unit_tests/modules/user/test_user_model.py::TestAuthModel::test_get_user_profiles PASSED                                              [57/73]
tests/unit_tests/modules/user/test_user_schema_validator.py::TestUpdateProfileSchemaValidators::test_update_profile_schema PASSED           [58/73]
tests/unit_tests/modules/user/test_user_view.py::TestProfile::test_get PASSED                                                               [59/73]
tests/unit_tests/modules/user/test_user_view.py::TestProfile::test_put PASSED                                                               [60/73]
tests/unit_tests/modules/user/test_user_view.py::TestProfiles::test_get PASSED                                                              [61/73]
tests/unit_tests/modules/user/test_user_view.py::TestProfiles2::test_get PASSED                                                             [62/73]
tests/unit_tests/modules/user/test_user_view.py::TestProfiles2::test_put PASSED                                                             [63/73]
tests/unit_tests/others/test_custom_exceptions.py::test_handle_exception PASSED                                                             [64/73]
tests/unit_tests/others/test_custom_exceptions.py::test_handle_custom_exception_error PASSED                                                [65/73]
tests/unit_tests/others/test_custom_exceptions.py::test_handle_unauthorized_user_error PASSED                                               [66/73]
tests/unit_tests/others/test_custom_exceptions.py::test_handle_record_not_found_error PASSED                                                [67/73]
tests/unit_tests/others/test_init_file.py::test_flask_env_not_set PASSED                                                                    [68/73]
tests/unit_tests/others/test_logger.py::test_logs_base_dir_creation PASSED                                                                  [69/73]
tests/unit_tests/others/test_logger.py::test_get_logger PASSED                                                                              [70/73]
tests/unit_tests/others/test_utils.py::test_get_generalize_query PASSED                                                                     [71/73]
tests/unit_tests/others/test_utils.py::test_get_data_from_request_or_raise_validation_error PASSED                                          [72/73]
tests/unit_tests/others/test_utils.py::test_log_user_access PASSED                                                                          [73/73]

=============================================================== 73 passed in 23.32s ===============================================================
Name                                           Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------
main\__init__.py                                  28      0   100%
main\custom_exceptions\__init__.py                 3      0   100%
main\custom_exceptions\exception_handlers.py      17      0   100%
main\custom_exceptions\exceptions.py              12      0   100%
main\db\__init__.py                               24      0   100%
main\logging_module\__init__.py                    4      0   100%
main\logging_module\logger.py                     19      0   100%
main\modules\__init__.py                          12      0   100%
main\modules\address\controller.py                38      0   100%
main\modules\address\model.py                     14      0   100%
main\modules\address\schema_validator.py          14      0   100%
main\modules\address\view.py                      39      0   100%
main\modules\auth\controller.py                   51      0   100%
main\modules\auth\model.py                        13      0   100%
main\modules\auth\schema_validator.py             20      0   100%
main\modules\auth\view.py                         42      0   100%
main\modules\jwt\controller.py                    27      0   100%
main\modules\jwt\model.py                          6      0   100%
main\modules\user\controller.py                   19      0   100%
main\modules\user\model.py                         9      0   100%
main\modules\user\schema_validator.py              7      0   100%
main\modules\user\view.py                         31      0   100%
main\utils.py                                     91      0   100%
----------------------------------------------------------------------------
TOTAL                                            540      0   100%

```

## Pre-Commit Hooks Setup
* Install Pre-commit hooks
```commandline
pre-commit install
```
* Run Pre-commit hooks. (Pre-commit hooks will run only on Staged Changes).
No need to run any command manually. It will auto run on git commit command.
But you can try to run it using the below command.
```commandline
pre-commit run
```
Output:
```commandline
PS C:\Users\PuneetDixit\Desktop\starter-kit>  pre-commit run

Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Isort (python)...........................................................Passed
Black....................................................................Passed
Flake8...................................................................Passed
Unit tests and code coverage.............................................Passed
Integration tests and code coverage......................................Passed
```
