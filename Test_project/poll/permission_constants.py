# Permissions name and code
# For model Personal
personal_add_permission = ('add_personal', 'Право добавлять сотрудника')
personal_change_permission = ('change_personal', 'Право изменять сотрудников')
personal_delete_permission = ('delete_personal', 'Право удалять сотрудников')
personal_view_permission = ('view_personal', 'Право смотреть сотрудников')
# For model Tests
tests_add_permission = ('add_tests', 'Право добавлять тесты')
tests_change_permission = ('change_tests', 'Право изменять тесты')
tests_delete_permission = ('delete_tests', 'Право удалять тесты')
tests_view_permission = ('view_tests', 'Право смотреть тесты')
# For model photo
photo_add_permission = ('add_photo', 'Право добавлять фото')
photo_change_permission = ('change_photo', 'Право изменять фото')
photo_delete_permission = ('delete_photo', 'Право удалять фото')
photo_view_permission = ('view_photo', 'Право смотреть фото')

# Permission list associated with groups
super_group_permissions = [personal_add_permission, personal_change_permission, personal_delete_permission,
                           personal_view_permission, tests_add_permission, tests_change_permission,
                            tests_delete_permission, tests_view_permission, photo_add_permission,
                           photo_change_permission, photo_delete_permission, photo_view_permission]
document_management_group_permissions = [personal_view_permission, tests_add_permission, tests_view_permission, photo_view_permission]
view_group_permission = [personal_view_permission, tests_view_permission, photo_view_permission]

# Group names
CUSTOMUSER_SUPER_GROUP = '_customuser_super_group'
CUSTOMUSER_DOCUMENT_MANAGEMENT_GROUP = '_customuser_add_tests_group'
CUSTOMUSER_VIEW_ONLY_GROUP = '_customuser_view_only_group'

# Group and permission list mappings
customuser_permission_group = {CUSTOMUSER_SUPER_GROUP: super_group_permissions,
                            CUSTOMUSER_VIEW_ONLY_GROUP: view_group_permission,
                            CUSTOMUSER_DOCUMENT_MANAGEMENT_GROUP: document_management_group_permissions}
















