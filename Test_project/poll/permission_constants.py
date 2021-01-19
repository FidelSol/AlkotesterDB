# Permissions name and code
archive_permission = ('_customuser_can_archive_permission', 'Can archive permission')
all_crud_permission = ('_customuser_can_do_all_crud_permission', 'Право действий CRUD - уровень руководителя')
view_only_permission = ('can_view_personal', 'Право просмотра - уровень менеджера, посетителя')
view_classified_information_permission = ('_customuser_can_view_classified_information',
                                          'Can view classified information')
document_management_permission = ('_customuser_can_upload_or_delete_tests',
                                  'Право добавить тесты - уровень проверяющего')

# Permission list associated with groups
super_group_permissions = [archive_permission, all_crud_permission, view_only_permission,
                           view_classified_information_permission,
                           document_management_permission]
document_management_group_permissions = [document_management_permission]
view_group_permission = [view_only_permission]
archive_group_permission = [archive_permission]

# Group names
CUSTOMUSER_SUPER_GROUP = '_customuser_super_group'
CUSTOMUSER_VIEW_ONLY_GROUP = '_customuser_view_only_group'
CUSTOMUSER_DOCUMENT_MANAGEMENT_GROUP = '_customuser_document_management_group'
CUSTOMUSER_ARCHIVE_GROUP = '_customuser_archive_group'

# Group and permission list mappings
customuser_permission_group = {CUSTOMUSER_SUPER_GROUP: super_group_permissions,
                            CUSTOMUSER_VIEW_ONLY_GROUP: view_group_permission,
                            CUSTOMUSER_DOCUMENT_MANAGEMENT_GROUP:
                                document_management_group_permissions,
                            CUSTOMUSER_ARCHIVE_GROUP: archive_group_permission}
















