"""Provides device triggers for Uonet+ Vulcan."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN

TRIGGER_TYPES = {
    "VREvent_None",
    "VREvent_TrackedDeviceActivated",
    "VREvent_TrackedDeviceDeactivated",
    "VREvent_TrackedDeviceUpdated",
    "VREvent_TrackedDeviceUserInteractionStarted",
    "VREvent_TrackedDeviceUserInteractionEnded",
    "VREvent_IpdChanged",
    "VREvent_EnterStandbyMode",
    "VREvent_LeaveStandbyMode",
    "VREvent_TrackedDeviceRoleChanged",
    "VREvent_WatchdogWakeUpRequested",
    "VREvent_LensDistortionChanged",
    "VREvent_PropertyChanged",
    "VREvent_WirelessDisconnect",
    "VREvent_WirelessReconnect",
    "VREvent_Reserved_01",
    "VREvent_Reserved_02",
    "VREvent_ButtonPress",
    "VREvent_ButtonUnpress",
    "VREvent_ButtonTouch",
    "VREvent_ButtonUntouch",
    "VREvent_Modal_Cancel",
    "VREvent_MouseMove",
    "VREvent_MouseButtonDown",
    "VREvent_MouseButtonUp",
    "VREvent_FocusEnter",
    "VREvent_FocusLeave",
    "VREvent_ScrollDiscrete",
    "VREvent_TouchPadMove",
    "VREvent_OverlayFocusChanged",
    "VREvent_ReloadOverlays",
    "VREvent_ScrollSmooth",
    "VREvent_LockMousePosition",
    "VREvent_UnlockMousePosition",
    "VREvent_InputFocusCaptured",
    "VREvent_InputFocusReleased",
    "VREvent_SceneApplicationChanged",
    "VREvent_InputFocusChanged",
    "VREvent_SceneApplicationUsingWrongGraphicsAdapter",
    "VREvent_ActionBindingReloaded",
    "VREvent_HideRenderModels",
    "VREvent_ShowRenderModels",
    "VREvent_SceneApplicationStateChanged",
    "VREvent_SceneAppPipeDisconnected",
    "VREvent_ConsoleOpened",
    "VREvent_ConsoleClosed",
    "VREvent_OverlayShown",
    "VREvent_OverlayHidden",
    "VREvent_DashboardActivated",
    "VREvent_DashboardDeactivated",
    "VREvent_DashboardRequested",
    "VREvent_ResetDashboard",
    "VREvent_ImageLoaded",
    "VREvent_ShowKeyboard",
    "VREvent_HideKeyboard",
    "VREvent_OverlayGamepadFocusGained",
    "VREvent_OverlayGamepadFocusLost",
    "VREvent_OverlaySharedTextureChanged",
    "VREvent_ScreenshotTriggered",
    "VREvent_ImageFailed",
    "VREvent_DashboardOverlayCreated",
    "VREvent_SwitchGamepadFocus",
    "VREvent_RequestScreenshot",
    "VREvent_ScreenshotTaken",
    "VREvent_ScreenshotFailed",
    "VREvent_SubmitScreenshotToDashboard",
    "VREvent_ScreenshotProgressToDashboard",
    "VREvent_PrimaryDashboardDeviceChanged",
    "VREvent_RoomViewShown",
    "VREvent_RoomViewHidden",
    "VREvent_ShowUI",
    "VREvent_ShowDevTools",
    "VREvent_DesktopViewUpdating",
    "VREvent_DesktopViewReady",
    "VREvent_StartDashboard",
    "VREvent_ElevatePrism",
    "VREvent_OverlayClosed",
    "VREvent_DashboardThumbChanged",
    "VREvent_DesktopMightBeVisible",
    "VREvent_DesktopMightBeHidden",
    "VREvent_Notification_Shown",
    "VREvent_Notification_Hidden",
    "VREvent_Notification_BeginInteraction",
    "VREvent_Notification_Destroyed",
    "VREvent_Quit",
    "VREvent_ProcessQuit",
    "VREvent_QuitAcknowledged",
    "VREvent_DriverRequestedQuit",
    "VREvent_RestartRequested",
    "VREvent_InvalidateSwapTextureSets",
    "VREvent_ChaperoneDataHasChanged",
    "VREvent_ChaperoneUniverseHasChanged",
    "VREvent_ChaperoneTempDataHasChanged",
    "VREvent_ChaperoneSettingsHaveChanged",
    "VREvent_SeatedZeroPoseReset",
    "VREvent_ChaperoneFlushCache",
    "VREvent_ChaperoneRoomSetupStarting",
    "VREvent_ChaperoneRoomSetupFinished",
    "VREvent_StandingZeroPoseReset",
    "VREvent_AudioSettingsHaveChanged",
    "VREvent_BackgroundSettingHasChanged",
    "VREvent_CameraSettingsHaveChanged",
    "VREvent_ReprojectionSettingHasChanged",
    "VREvent_ModelSkinSettingsHaveChanged",
    "VREvent_EnvironmentSettingsHaveChanged",
    "VREvent_PowerSettingsHaveChanged",
    "VREvent_EnableHomeAppSettingsHaveChanged",
    "VREvent_SteamVRSectionSettingChanged",
    "VREvent_LighthouseSectionSettingChanged",
    "VREvent_NullSectionSettingChanged",
    "VREvent_UserInterfaceSectionSettingChanged",
    "VREvent_NotificationsSectionSettingChanged",
    "VREvent_KeyboardSectionSettingChanged",
    "VREvent_PerfSectionSettingChanged",
    "VREvent_DashboardSectionSettingChanged",
    "VREvent_WebInterfaceSectionSettingChanged",
    "VREvent_TrackersSectionSettingChanged",
    "VREvent_LastKnownSectionSettingChanged",
    "VREvent_DismissedWarningsSectionSettingChanged",
    "VREvent_GpuSpeedSectionSettingChanged",
    "VREvent_WindowsMRSectionSettingChanged",
    "VREvent_OtherSectionSettingChanged",
    "VREvent_AnyDriverSettingsChanged",
    "VREvent_StatusUpdate",
    "VREvent_WebInterface_InstallDriverCompleted",
    "VREvent_MCImageUpdated",
    "VREvent_FirmwareUpdateStarted",
    "VREvent_FirmwareUpdateFinished",
    "VREvent_KeyboardClosed",
    "VREvent_KeyboardCharInput",
    "VREvent_KeyboardDone",
    "VREvent_KeyboardOpened_Global",
    "VREvent_KeyboardClosed_Global",
    "VREvent_ApplicationListUpdated",
    "VREvent_ApplicationMimeTypeLoad",
    "VREvent_ProcessConnected",
    "VREvent_ProcessDisconnected",
    "VREvent_Compositor_ChaperoneBoundsShown",
    "VREvent_Compositor_ChaperoneBoundsHidden",
    "VREvent_Compositor_DisplayDisconnected",
    "VREvent_Compositor_DisplayReconnected",
    "VREvent_Compositor_HDCPError",
    "VREvent_Compositor_ApplicationNotResponding",
    "VREvent_Compositor_ApplicationResumed",
    "VREvent_Compositor_OutOfVideoMemory",
    "VREvent_Compositor_DisplayModeNotSupported",
    "VREvent_Compositor_StageOverrideReady",
    "VREvent_Compositor_RequestDisconnectReconnect",
    "VREvent_TrackedCamera_StartVideoStream",
    "VREvent_TrackedCamera_StopVideoStream",
    "VREvent_TrackedCamera_PauseVideoStream",
    "VREvent_TrackedCamera_ResumeVideoStream",
    "VREvent_TrackedCamera_EditingSurface",
    "VREvent_PerformanceTest_EnableCapture",
    "VREvent_PerformanceTest_DisableCapture",
    "VREvent_PerformanceTest_FidelityLevel",
    "VREvent_MessageOverlay_Closed",
    "VREvent_MessageOverlayCloseRequested",
    "VREvent_Input_HapticVibration",
    "VREvent_Input_BindingLoadFailed",
    "VREvent_Input_BindingLoadSuccessful",
    "VREvent_Input_ActionManifestReloaded",
    "VREvent_Input_ActionManifestLoadFailed",
    "VREvent_Input_ProgressUpdate",
    "VREvent_Input_TrackerActivated",
    "VREvent_Input_BindingsUpdated",
    "VREvent_Input_BindingSubscriptionChanged",
    "VREvent_SpatialAnchors_PoseUpdated",
    "VREvent_SpatialAnchors_DescriptorUpdated",
    "VREvent_SpatialAnchors_RequestPoseUpdate",
    "VREvent_SpatialAnchors_RequestDescriptorUpdate",
    "VREvent_SystemReport_Started",
    "VREvent_Monitor_ShowHeadsetView",
    "VREvent_Monitor_HideHeadsetView",
    "VREvent_Audio_SetSpeakersVolume",
    "VREvent_Audio_SetSpeakersMute",
    "VREvent_Audio_SetMicrophoneVolume",
    "VREvent_Audio_SetMicrophoneMute",
    "VREvent_VendorSpecific_Reserved_Start",
    "VREvent_VendorSpecific_Reserved_End",
}

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(hass, device_id):
    """Return a list of triggers."""

    device_registry = dr.async_get(hass)
    device = device_registry.async_get(device_id)

    triggers = []

    if device is None:
        return triggers

    for entry in er.async_entries_for_device(er.async_get(hass), device_id):
        if f"{entry.config_entry_id}_vr_status" not in list(device.identifiers)[0]:
            continue
        for trigger in TRIGGER_TYPES:
            triggers.append(
                {
                    # Required fields of TRIGGER_BASE_SCHEMA
                    CONF_PLATFORM: "device",
                    CONF_DOMAIN: DOMAIN,
                    CONF_DEVICE_ID: device_id,
                    # Required fields of TRIGGER_SCHEMA
                    CONF_TYPE: trigger,
                }
            )

    return triggers


async def async_attach_trigger(hass, config, action, trigger_info):
    """Attach a trigger."""
    event_config = event_trigger.TRIGGER_SCHEMA(
        {
            event_trigger.CONF_PLATFORM: "event",
            event_trigger.CONF_EVENT_TYPE: "steamvr_event",
            event_trigger.CONF_EVENT_DATA: {
                CONF_DEVICE_ID: config[CONF_DEVICE_ID],
                CONF_TYPE: config[CONF_TYPE],
            },
        }
    )
    return await event_trigger.async_attach_trigger(
        hass, event_config, action, trigger_info, platform_type="device"
    )
