from typing import Any

MAJOR_PARAMS: Any # TODO

class Route:
  def __init__(self, method, path, **params) -> None: ...

  method: Any # TODO
  path: Any # TODO
  key: Any # TODO
  major: Any # TODO

class API:
  """
  TODO
  """

  async def request(self, route: Route, *, body: Any = ..., authorize: bool | str = ..., reason: str | None = ..., **params: Any) -> Any:
    """
    TODO

    Args:
      route: TODO
      body: TODO
      authorize: TODO
      reason: TODO
      **params: TODO

    Returns:
      TODO
    """

  async def list_application_commands(self, application_id, with_localizations = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      with_localizations: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def create_application_command(self, application_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_application_command(self, application_id, command_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      command_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def update_application_command(self, application_id, command_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      command_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def delete_application_command(self, application_id, command_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      command_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def bulk_overwrite_global_commands(self, application_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def list_guild_application_commands(self, application_id, guild_id, with_localizations = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      with_localizations: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def create_guild_application_command(self, application_id, guild_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_guild_application_command(self, application_id, guild_id, command_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      command_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def update_guild_application_command(self, application_id, guild_id, command_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      command_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def delete_guild_application_command(self, application_id, guild_id, command_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      command_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def bulk_set_guild_application_commands(self, application_id, guild_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def list_guild_application_command_permissions(self, application_id, guild_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_guild_application_command_permissions(self, application_id, guild_id, command_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      command_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def set_guild_application_command_permissions(self, application_id, guild_id, command_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      guild_id: TODO
      command_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_my_application(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def update_my_application(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def applications_get_activity_instance(self, application_id, instance_id) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      instance_id: TODO

    Returns:
      TODO
    """

  async def get_application_role_connections_metadata(self, application_id) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO

    Returns:
      TODO
    """

  async def update_application_role_connections_metadata(self, application_id, data) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def list_guild_audit_log_entries(self, guild_id, user_id = ..., target_id = ..., action_type = ..., before = ..., after = ..., limit = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO
      target_id: TODO
      action_type: TODO
      before: TODO
      after: TODO
      limit: TODO

    Returns:
      TODO
    """

  async def list_auto_moderation_rules(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_auto_moderation_rule(self, guild_id, rule_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      rule_id: TODO

    Returns:
      TODO
    """

  async def create_auto_moderation_rule(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_auto_moderation_rule(self, guild_id, rule_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      rule_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_auto_moderation_rule(self, guild_id, rule_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      rule_id: TODO

    Returns:
      TODO
    """

  async def get_channel(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def update_channel(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_voice_channel_status(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_channel(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def set_channel_permission_overwrite(self, channel_id, overwrite_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      overwrite_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def list_channel_invites(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def create_channel_invite(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_channel_permission_overwrite(self, channel_id, overwrite_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      overwrite_id: TODO

    Returns:
      TODO
    """

  async def follow_channel(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def trigger_typing_indicator(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def add_group_dm_user(self, channel_id, user_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      user_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_group_dm_user(self, channel_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def create_thread_from_message(self, channel_id, message_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def create_thread(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def join_thread(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def add_thread_member(self, channel_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def leave_thread(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def delete_thread_member(self, channel_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def get_thread_member(self, channel_id, user_id, with_member = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      user_id: TODO
      with_member: TODO

    Returns:
      TODO
    """

  async def list_thread_members(self, channel_id, with_member = ..., limit = ..., after = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      with_member: TODO
      limit: TODO
      after: TODO

    Returns:
      TODO
    """

  async def list_public_archived_threads(self, channel_id, before = ..., limit = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      before: TODO
      limit: TODO

    Returns:
      TODO
    """

  async def list_private_archived_threads(self, channel_id, before = ..., limit = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      before: TODO
      limit: TODO

    Returns:
      TODO
    """

  async def list_my_private_archived_threads(self, channel_id, before = ..., limit = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      before: TODO
      limit: TODO

    Returns:
      TODO
    """

  async def list_guild_emojis(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_guild_emoji(self, guild_id, emoji_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      emoji_id: TODO

    Returns:
      TODO
    """

  async def create_guild_emoji(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_guild_emoji(self, guild_id, emoji_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      emoji_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_guild_emoji(self, guild_id, emoji_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      emoji_id: TODO

    Returns:
      TODO
    """

  async def list_application_emojis(self, application_id) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO

    Returns:
      TODO
    """

  async def get_application_emoji(self, application_id, emoji_id) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      emoji_id: TODO

    Returns:
      TODO
    """

  async def create_application_emoji(self, application_id, data) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_application_emoji(self, application_id, emoji_id, data) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      emoji_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_application_emoji(self, application_id, emoji_id) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      emoji_id: TODO

    Returns:
      TODO
    """

  async def get_entitlements(self, application_id, user_id = ..., sku_ids = ..., guild_id = ..., before = ..., after = ..., limit = ..., exclude_ended = ..., exclude_deleted = ..., only_active = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      user_id: TODO
      sku_ids: TODO
      guild_id: TODO
      before: TODO
      after: TODO
      limit: TODO
      exclude_ended: TODO
      exclude_deleted: TODO
      only_active: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_entitlement(self, application_id, entitlement_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      entitlement_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def consume_entitlement(self, application_id, entitlement_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      entitlement_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def create_entitlement(self, application_id, data) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_entitlement(self, application_id, entitlement_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      entitlement_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_gateway(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def get_bot_gateway(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def get_guild(self, guild_id, with_counts = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      with_counts: TODO

    Returns:
      TODO
    """

  async def get_guild_preview(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def update_guild(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def list_guild_channels(self, guild_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def create_guild_channel(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def bulk_update_guild_channels(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def get_active_guild_threads(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_guild_member(self, guild_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def list_guild_members(self, guild_id, limit = ..., after = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      limit: TODO
      after: TODO

    Returns:
      TODO
    """

  async def search_guild_members(self, guild_id, limit = ..., query = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      limit: TODO
      query: TODO

    Returns:
      TODO
    """

  async def add_guild_member(self, guild_id, user_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_guild_member(self, guild_id, user_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_my_guild_member(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def add_guild_member_role(self, guild_id, user_id, role_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO
      role_id: TODO

    Returns:
      TODO
    """

  async def delete_guild_member_role(self, guild_id, user_id, role_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO
      role_id: TODO

    Returns:
      TODO
    """

  async def delete_guild_member(self, guild_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def list_guild_bans(self, guild_id, limit = ..., before = ..., after = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      limit: TODO
      before: TODO
      after: TODO

    Returns:
      TODO
    """

  async def get_guild_ban(self, guild_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def ban_user_from_guild(self, guild_id, user_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def unban_user_from_guild(self, guild_id, user_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def bulk_ban_users_from_guild(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def list_guild_roles(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_guild_role(self, guild_id, role_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      role_id: TODO

    Returns:
      TODO
    """

  async def guild_role_member_counts(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def create_guild_role(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def bulk_update_guild_roles(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_guild_role(self, guild_id, role_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      role_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_guild_role(self, guild_id, role_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      role_id: TODO

    Returns:
      TODO
    """

  async def preview_prune_guild(self, guild_id, days = ..., include_roles = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      days: TODO
      include_roles: TODO

    Returns:
      TODO
    """

  async def prune_guild(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def list_guild_voice_regions(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def list_guild_invites(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def list_guild_integrations(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def delete_guild_integration(self, guild_id, integration_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      integration_id: TODO

    Returns:
      TODO
    """

  async def get_guild_widget_settings(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def update_guild_widget_settings(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def get_guild_widget(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_guild_vanity_url(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_guild_widget_png(self, guild_id, style = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      style: TODO

    Returns:
      TODO
    """

  async def get_guild_welcome_screen(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def update_guild_welcome_screen(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def get_guilds_onboarding(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def put_guilds_onboarding(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_guild_incident_actions(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def list_guild_scheduled_events(self, guild_id, with_user_count = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      with_user_count: TODO

    Returns:
      TODO
    """

  async def create_guild_scheduled_event(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def get_guild_scheduled_event(self, guild_id, guild_scheduled_event_id, with_user_count = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO
      with_user_count: TODO

    Returns:
      TODO
    """

  async def update_guild_scheduled_event(self, guild_id, guild_scheduled_event_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_guild_scheduled_event(self, guild_id, guild_scheduled_event_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO

    Returns:
      TODO
    """

  async def list_guild_scheduled_event_users(self, guild_id, guild_scheduled_event_id, with_member = ..., limit = ..., before = ..., after = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO
      with_member: TODO
      limit: TODO
      before: TODO
      after: TODO

    Returns:
      TODO
    """

  async def get_guild_template(self, code) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO

    Returns:
      TODO
    """

  async def list_guild_templates(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def create_guild_template(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def sync_guild_template(self, guild_id, code) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      code: TODO

    Returns:
      TODO
    """

  async def update_guild_template(self, guild_id, code, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      code: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_guild_template(self, guild_id, code) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      code: TODO

    Returns:
      TODO
    """

  async def invite_resolve(self, code, with_counts = ..., guild_scheduled_event_id = ..., target_channel_id = ..., target_message_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO
      with_counts: TODO
      guild_scheduled_event_id: TODO
      target_channel_id: TODO
      target_message_id: TODO

    Returns:
      TODO
    """

  async def invite_revoke(self, code) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO

    Returns:
      TODO
    """

  async def get_invite_target_users(self, code) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO

    Returns:
      TODO
    """

  async def add_invite_target_user(self, code, user_id) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def remove_invite_target_user(self, code, user_id) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def update_invite_target_users(self, code, data) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO
      data: TODO

    Returns:
      TODO
    """

  async def bulk_add_invite_target_users(self, code, data) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO
      data: TODO

    Returns:
      TODO
    """

  async def bulk_remove_invite_target_users(self, code, data) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO
      data: TODO

    Returns:
      TODO
    """

  async def get_invite_target_users_job_status(self, code) -> Any: # TODO
    """
    TODO

    Args:
      code: TODO

    Returns:
      TODO
    """

  async def create_lobby(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def create_or_join_lobby(self, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_lobby(self, lobby_id) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO

    Returns:
      TODO
    """

  async def edit_lobby(self, lobby_id, data) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_lobby(self, lobby_id) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO

    Returns:
      TODO
    """

  async def add_lobby_member(self, lobby_id, user_id, data) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      user_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def bulk_update_lobby_members(self, lobby_id, data) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_lobby_member(self, lobby_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def leave_lobby(self, lobby_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def edit_lobby_channel_link(self, lobby_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def create_lobby_message(self, lobby_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_lobby_messages(self, lobby_id, limit = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      limit: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def update_lobby_message_external_moderation_metadata(self, lobby_id, message_id, data) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      message_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def create_linked_lobby_guild_invite_for_self(self, lobby_id, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def create_linked_lobby_guild_invite_for_user(self, lobby_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      lobby_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def list_messages(self, channel_id, around = ..., before = ..., after = ..., limit = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      around: TODO
      before: TODO
      after: TODO
      limit: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def guild_search(self, guild_id, sort_by = ..., sort_order = ..., content = ..., slop = ..., author_id = ..., author_type = ..., mentions = ..., mentions_role_id = ..., replied_to_user_id = ..., replied_to_message_id = ..., mention_everyone = ..., min_id = ..., max_id = ..., limit = ..., offset = ..., has = ..., link_hostname = ..., embed_provider = ..., embed_type = ..., attachment_extension = ..., attachment_filename = ..., pinned = ..., include_nsfw = ..., channel_id = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      sort_by: TODO
      sort_order: TODO
      content: TODO
      slop: TODO
      author_id: TODO
      author_type: TODO
      mentions: TODO
      mentions_role_id: TODO
      replied_to_user_id: TODO
      replied_to_message_id: TODO
      mention_everyone: TODO
      min_id: TODO
      max_id: TODO
      limit: TODO
      offset: TODO
      has: TODO
      link_hostname: TODO
      embed_provider: TODO
      embed_type: TODO
      attachment_extension: TODO
      attachment_filename: TODO
      pinned: TODO
      include_nsfw: TODO
      channel_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_message(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def create_message(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def crosspost_message(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def add_my_message_reaction(self, channel_id, message_id, emoji_name) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO
      emoji_name: TODO

    Returns:
      TODO
    """

  async def delete_my_message_reaction(self, channel_id, message_id, emoji_name) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO
      emoji_name: TODO

    Returns:
      TODO
    """

  async def delete_user_message_reaction(self, channel_id, message_id, emoji_name, user_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO
      emoji_name: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def list_message_reactions_by_emoji(self, channel_id, message_id, emoji_name, after = ..., limit = ..., type = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO
      emoji_name: TODO
      after: TODO
      limit: TODO
      type: TODO

    Returns:
      TODO
    """

  async def delete_all_message_reactions(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def delete_all_message_reactions_by_emoji(self, channel_id, message_id, emoji_name) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO
      emoji_name: TODO

    Returns:
      TODO
    """

  async def edit_message(self, channel_id, message_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_message(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def bulk_delete_messages(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def list_pins(self, channel_id, before = ..., limit = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      before: TODO
      limit: TODO

    Returns:
      TODO
    """

  async def create_pin(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def delete_pin(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def deprecated_list_pins(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def deprecated_create_pin(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def deprecated_delete_pin(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def get_my_oauth2_application(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def get_my_oauth2_authorization(self, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      authorize: TODO

    Returns:
      TODO
    """

  async def get_answer_voters(self, channel_id, message_id, answer_id, after = ..., limit = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO
      answer_id: TODO
      after: TODO
      limit: TODO

    Returns:
      TODO
    """

  async def poll_expire(self, channel_id, message_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      message_id: TODO

    Returns:
      TODO
    """

  async def create_interaction_response(self, interaction_id, interaction_token, data, with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      interaction_id: TODO
      interaction_token: TODO
      data: TODO
      with_response: TODO

    Returns:
      TODO
    """

  async def get_original_webhook_message(self, webhook_id, webhook_token, thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  async def update_original_webhook_message(self, webhook_id, webhook_token, data, thread_id = ..., with_components = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      data: TODO
      thread_id: TODO
      with_components: TODO

    Returns:
      TODO
    """

  async def delete_original_webhook_message(self, webhook_id, webhook_token, thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  async def send_soundboard_sound(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def get_soundboard_default_sounds(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def list_guild_soundboard_sounds(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_guild_soundboard_sound(self, guild_id, sound_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      sound_id: TODO

    Returns:
      TODO
    """

  async def create_guild_soundboard_sound(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_guild_soundboard_sound(self, guild_id, sound_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      sound_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_guild_soundboard_sound(self, guild_id, sound_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      sound_id: TODO

    Returns:
      TODO
    """

  async def create_stage_instance(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def get_stage_instance(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def update_stage_instance(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_stage_instance(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def get_sticker(self, sticker_id) -> Any: # TODO
    """
    TODO

    Args:
      sticker_id: TODO

    Returns:
      TODO
    """

  async def list_sticker_packs(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def get_sticker_pack(self, pack_id) -> Any: # TODO
    """
    TODO

    Args:
      pack_id: TODO

    Returns:
      TODO
    """

  async def list_guild_stickers(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_guild_sticker(self, guild_id, sticker_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      sticker_id: TODO

    Returns:
      TODO
    """

  async def create_guild_sticker(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_guild_sticker(self, guild_id, sticker_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      sticker_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_guild_sticker(self, guild_id, sticker_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      sticker_id: TODO

    Returns:
      TODO
    """

  async def get_sku_subscriptions(self, sku_id, before = ..., after = ..., limit = ..., user_id = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      sku_id: TODO
      before: TODO
      after: TODO
      limit: TODO
      user_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_sku_subscription(self, sku_id, subscription_id, user_id = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      sku_id: TODO
      subscription_id: TODO
      user_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_my_user(self, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      authorize: TODO

    Returns:
      TODO
    """

  async def get_user(self, user_id) -> Any: # TODO
    """
    TODO

    Args:
      user_id: TODO

    Returns:
      TODO
    """

  async def update_my_user(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def list_my_guilds(self, before = ..., after = ..., limit = ..., shard = ..., with_counts = ..., authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      before: TODO
      after: TODO
      limit: TODO
      shard: TODO
      with_counts: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def get_my_guild_member(self, guild_id, authorize: str) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def leave_guild(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def create_dm(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def list_my_connections(self, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      authorize: TODO

    Returns:
      TODO
    """

  async def get_application_user_role_connection(self, application_id, authorize: str) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def update_application_user_role_connection(self, application_id, authorize: str, data) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      authorize: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_application_user_role_connection(self, application_id, authorize: str) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def list_voice_regions(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def get_self_voice_state(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_voice_state(self, guild_id, user_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO

    Returns:
      TODO
    """

  async def update_self_voice_state(self, guild_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_voice_state(self, guild_id, user_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      user_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def create_webhook(self, channel_id, data) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def list_channel_webhooks(self, channel_id) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO

    Returns:
      TODO
    """

  async def get_guild_webhooks(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_webhook(self, webhook_id) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO

    Returns:
      TODO
    """

  async def get_webhook_by_token(self, webhook_id, webhook_token) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO

    Returns:
      TODO
    """

  async def update_webhook(self, webhook_id, data) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def update_webhook_by_token(self, webhook_id, webhook_token, data) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_webhook(self, webhook_id) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO

    Returns:
      TODO
    """

  async def delete_webhook_by_token(self, webhook_id, webhook_token) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO

    Returns:
      TODO
    """

  async def execute_webhook(self, webhook_id, webhook_token, data, wait = ..., thread_id = ..., with_components = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      data: TODO
      wait: TODO
      thread_id: TODO
      with_components: TODO

    Returns:
      TODO
    """

  async def execute_slack_compatible_webhook(self, webhook_id, webhook_token, data, wait = ..., thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      data: TODO
      wait: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  async def execute_github_compatible_webhook(self, webhook_id, webhook_token, data, wait = ..., thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      data: TODO
      wait: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  async def get_webhook_message(self, webhook_id, webhook_token, message_id, thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      message_id: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  async def update_webhook_message(self, webhook_id, webhook_token, message_id, data, thread_id = ..., with_components = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      message_id: TODO
      data: TODO
      thread_id: TODO
      with_components: TODO

    Returns:
      TODO
    """

  async def delete_webhook_message(self, webhook_id, webhook_token, message_id, thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      webhook_token: TODO
      message_id: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  async def get_application(self, application_id) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO

    Returns:
      TODO
    """

  async def update_application(self, application_id, data) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def upload_application_attachment(self, application_id, data, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      data: TODO
      authorize: TODO

    Returns:
      TODO
    """

  async def thread_search(self, channel_id, name = ..., slop = ..., min_id = ..., max_id = ..., tag = ..., tag_setting = ..., archived = ..., sort_by = ..., sort_order = ..., limit = ..., offset = ...) -> Any: # TODO
    """
    TODO

    Args:
      channel_id: TODO
      name: TODO
      slop: TODO
      min_id: TODO
      max_id: TODO
      tag: TODO
      tag_setting: TODO
      archived: TODO
      sort_by: TODO
      sort_order: TODO
      limit: TODO
      offset: TODO

    Returns:
      TODO
    """

  async def get_guild_new_member_welcome(self, guild_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO

    Returns:
      TODO
    """

  async def get_guild_join_requests(self, guild_id, status = ..., limit = ..., before = ..., after = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      status: TODO
      limit: TODO
      before: TODO
      after: TODO

    Returns:
      TODO
    """

  async def action_guild_join_request(self, guild_id, request_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      request_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def create_guild_scheduled_event_exception(self, guild_id, guild_scheduled_event_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def delete_guild_scheduled_event_exception(self, guild_id, guild_scheduled_event_id, exception_id) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO
      exception_id: TODO

    Returns:
      TODO
    """

  async def update_guild_scheduled_event_exception(self, guild_id, guild_scheduled_event_id, exception_id, data) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO
      exception_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def count_guild_scheduled_event_users(self, guild_id, guild_scheduled_event_id, guild_scheduled_event_exception_ids = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO
      guild_scheduled_event_exception_ids: TODO

    Returns:
      TODO
    """

  async def list_guild_scheduled_event_exception_users(self, guild_id, guild_scheduled_event_id, guild_scheduled_event_exception_id, with_member = ..., limit = ..., before = ..., after = ...) -> Any: # TODO
    """
    TODO

    Args:
      guild_id: TODO
      guild_scheduled_event_id: TODO
      guild_scheduled_event_exception_id: TODO
      with_member: TODO
      limit: TODO
      before: TODO
      after: TODO

    Returns:
      TODO
    """

  async def get_public_keys(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def get_openid_connect_userinfo(self, authorize: bool | str = ...) -> Any: # TODO
    """
    TODO

    Args:
      authorize: TODO

    Returns:
      TODO
    """

  async def update_user_message_external_moderation_metadata(self, user_id_1, user_id_2, message_id, data) -> Any: # TODO
    """
    TODO

    Args:
      user_id_1: TODO
      user_id_2: TODO
      message_id: TODO
      data: TODO

    Returns:
      TODO
    """

  async def partner_sdk_unmerge_provisional_account(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def bot_partner_sdk_unmerge_provisional_account(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def partner_sdk_token(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def bot_partner_sdk_token(self, data) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO

    Returns:
      TODO
    """

  async def get_current_user_application_entitlements(self, application_id, authorize: str, sku_ids = ..., exclude_consumed = ...) -> Any: # TODO
    """
    TODO

    Args:
      application_id: TODO
      authorize: TODO
      sku_ids: TODO
      exclude_consumed: TODO

    Returns:
      TODO
    """
