from pyramid.security import Allow


__acl__ = [
    (Allow, 'group:__admin__', 'admin_index'),
    (Allow, 'group:__staff__', 'admin_index'),
    (Allow, 'group:__admin__', 'admin_features'),
    (Allow, 'group:__admin__', 'admin_nipsa'),
    (Allow, 'group:__admin__', 'admin_admins'),
    (Allow, 'group:__admin__', 'admin_reports'),
    (Allow, 'group:__staff__', 'admin_reports'),
    (Allow, 'group:__admin__', 'admin_staff'),
    (Allow, 'group:__admin__', 'admin_users'),
    (Allow, 'group:__staff__', 'admin_users'),
    (Allow, 'group:__admin__', 'admin_badge'),
    (Allow, 'group:__admin__', 'admin_groups'),
    (Allow, 'group:__staff__', 'admin_groups'),
    (Allow, 'group:__staff__', 'admin_view_translation'),
    (Allow, 'group:__admin__', 'admin_view_translation'),
    (Allow, 'group:__staff__', 'admin_delete_translation'),
    (Allow, 'group:__admin__', 'admin_delete_translation'),
    (Allow, 'group:__staff__', 'admin_delete_block_translation'),
    (Allow, 'group:__admin__', 'admin_delete_block_translation'),
    (Allow, 'group:__staff__', 'admin_delete_report'),
    (Allow, 'group:__admin__', 'admin_delete_report'),
]