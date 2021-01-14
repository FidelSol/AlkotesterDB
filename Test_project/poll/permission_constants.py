# Permissions name and code
archive_permission = ('can_archive_permission', 'Can archive permission')
all_crud_permission = ('can_do_all_crud_permission', 'Can do all crud')
view_only_permission = ('can_view_only_permission', 'Can view only permission')
view_classified_information_permission = ('can_view_classified_information',
                                          'Can view classified information')
document_management_permission = ('can_upload_or_delete_tests',
                                  'Can upload or delete tests')

# Permission list associated with groups
super_group_permissions = [archive_permission, all_crud_permission, view_only_permission,
                           view_classified_information_permission,
                           document_management_permission]
document_management_group_permissions = [document_management_permission]
view_group_permission = [view_only_permission]
archive_group_permission = [archive_permission]

# Group names
SUPER_GROUP = '_super_group'
VIEW_ONLY_GROUP = '_view_only_group'
DOCUMENT_MANAGEMENT_GROUP = '_document_management_group'
ARCHIVE_GROUP = '_archive_group'

# Group and permission list mappings
permission_group = {SUPER_GROUP: super_group_permissions,
                            VIEW_ONLY_GROUP: view_group_permission,
                            DOCUMENT_MANAGEMENT_GROUP:
                                document_management_group_permissions,
                            ARCHIVE_GROUP: archive_group_permission}
















