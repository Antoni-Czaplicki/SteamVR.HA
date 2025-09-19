"""Utility functions for SteamVR Home Assistant integration."""

VR_EVENT_MAPPING = {
    "VREvent_None": "vr-event-none",
    "VREvent_TrackedDeviceActivated": "vr-event-tracked-device-activated",
    "VREvent_TrackedDeviceDeactivated": "vr-event-tracked-device-deactivated",
    "VREvent_TrackedDeviceUpdated": "vr-event-tracked-device-updated",
    "VREvent_TrackedDeviceUserInteractionStarted": "vr-event-tracked-device-user-interaction-started",
    "VREvent_TrackedDeviceUserInteractionEnded": "vr-event-tracked-device-user-interaction-ended",
    "VREvent_IpdChanged": "vr-event-ipd-changed",
    "VREvent_EnterStandbyMode": "vr-event-enter-standby-mode",
    "VREvent_LeaveStandbyMode": "vr-event-leave-standby-mode",
    "VREvent_TrackedDeviceRoleChanged": "vr-event-tracked-device-role-changed",
    "VREvent_WatchdogWakeUpRequested": "vr-event-watchdog-wake-up-requested",
    "VREvent_LensDistortionChanged": "vr-event-lens-distortion-changed",
    "VREvent_PropertyChanged": "vr-event-property-changed",
    "VREvent_WirelessDisconnect": "vr-event-wireless-disconnect",
    "VREvent_WirelessReconnect": "vr-event-wireless-reconnect",
    "VREvent_Reserved_01": "vr-event-reserved-01",
    "VREvent_Reserved_02": "vr-event-reserved-02",
    "VREvent_ButtonPress": "vr-event-button-press",
    "VREvent_ButtonUnpress": "vr-event-button-unpress",
    "VREvent_ButtonTouch": "vr-event-button-touch",
    "VREvent_ButtonUntouch": "vr-event-button-untouch",
    "VREvent_Modal_Cancel": "vr-event-modal-cancel",
    "VREvent_MouseMove": "vr-event-mouse-move",
    "VREvent_MouseButtonDown": "vr-event-mouse-button-down",
    "VREvent_MouseButtonUp": "vr-event-mouse-button-up",
    "VREvent_FocusEnter": "vr-event-focus-enter",
    "VREvent_FocusLeave": "vr-event-focus-leave",
    "VREvent_ScrollDiscrete": "vr-event-scroll-discrete",
    "VREvent_TouchPadMove": "vr-event-touch-pad-move",
    "VREvent_OverlayFocusChanged": "vr-event-overlay-focus-changed",
    "VREvent_ReloadOverlays": "vr-event-reload-overlays",
    "VREvent_ScrollSmooth": "vr-event-scroll-smooth",
    "VREvent_LockMousePosition": "vr-event-lock-mouse-position",
    "VREvent_UnlockMousePosition": "vr-event-unlock-mouse-position",
    "VREvent_InputFocusCaptured": "vr-event-input-focus-captured",
    "VREvent_InputFocusReleased": "vr-event-input-focus-released",
    "VREvent_SceneApplicationChanged": "vr-event-scene-application-changed",
    "VREvent_InputFocusChanged": "vr-event-input-focus-changed",
    "VREvent_SceneApplicationUsingWrongGraphicsAdapter": "vr-event-scene-application-using-wrong-graphics-adapter",
    "VREvent_ActionBindingReloaded": "vr-event-action-binding-reloaded",
    "VREvent_HideRenderModels": "vr-event-hide-render-models",
    "VREvent_ShowRenderModels": "vr-event-show-render-models",
    "VREvent_SceneApplicationStateChanged": "vr-event-scene-application-state-changed",
    "VREvent_SceneAppPipeDisconnected": "vr-event-scene-app-pipe-disconnected",
    "VREvent_ConsoleOpened": "vr-event-console-opened",
    "VREvent_ConsoleClosed": "vr-event-console-closed",
    "VREvent_OverlayShown": "vr-event-overlay-shown",
    "VREvent_OverlayHidden": "vr-event-overlay-hidden",
    "VREvent_DashboardActivated": "vr-event-dashboard-activated",
    "VREvent_DashboardDeactivated": "vr-event-dashboard-deactivated",
    "VREvent_DashboardRequested": "vr-event-dashboard-requested",
    "VREvent_ResetDashboard": "vr-event-reset-dashboard",
    "VREvent_ImageLoaded": "vr-event-image-loaded",
    "VREvent_ShowKeyboard": "vr-event-show-keyboard",
    "VREvent_HideKeyboard": "vr-event-hide-keyboard",
    "VREvent_OverlayGamepadFocusGained": "vr-event-overlay-gamepad-focus-gained",
    "VREvent_OverlayGamepadFocusLost": "vr-event-overlay-gamepad-focus-lost",
    "VREvent_OverlaySharedTextureChanged": "vr-event-overlay-shared-texture-changed",
    "VREvent_ScreenshotTriggered": "vr-event-screenshot-triggered",
    "VREvent_ImageFailed": "vr-event-image-failed",
    "VREvent_DashboardOverlayCreated": "vr-event-dashboard-overlay-created",
    "VREvent_SwitchGamepadFocus": "vr-event-switch-gamepad-focus",
    "VREvent_RequestScreenshot": "vr-event-request-screenshot",
    "VREvent_ScreenshotTaken": "vr-event-screenshot-taken",
    "VREvent_ScreenshotFailed": "vr-event-screenshot-failed",
    "VREvent_SubmitScreenshotToDashboard": "vr-event-submit-screenshot-to-dashboard",
    "VREvent_ScreenshotProgressToDashboard": "vr-event-screenshot-progress-to-dashboard",
    "VREvent_PrimaryDashboardDeviceChanged": "vr-event-primary-dashboard-device-changed",
    "VREvent_RoomViewShown": "vr-event-room-view-shown",
    "VREvent_RoomViewHidden": "vr-event-room-view-hidden",
    "VREvent_ShowUI": "vr-event-show-ui",
    "VREvent_ShowDevTools": "vr-event-show-dev-tools",
    "VREvent_DesktopViewUpdating": "vr-event-desktop-view-updating",
    "VREvent_DesktopViewReady": "vr-event-desktop-view-ready",
    "VREvent_StartDashboard": "vr-event-start-dashboard",
    "VREvent_ElevatePrism": "vr-event-elevate-prism",
    "VREvent_OverlayClosed": "vr-event-overlay-closed",
    "VREvent_DashboardThumbChanged": "vr-event-dashboard-thumb-changed",
    "VREvent_DesktopMightBeVisible": "vr-event-desktop-might-be-visible",
    "VREvent_DesktopMightBeHidden": "vr-event-desktop-might-be-hidden",
    "VREvent_Notification_Shown": "vr-event-notification-shown",
    "VREvent_Notification_Hidden": "vr-event-notification-hidden",
    "VREvent_Notification_BeginInteraction": "vr-event-notification-begin-interaction",
    "VREvent_Notification_Destroyed": "vr-event-notification-destroyed",
    "VREvent_Quit": "vr-event-quit",
    "VREvent_ProcessQuit": "vr-event-process-quit",
    "VREvent_QuitAcknowledged": "vr-event-quit-acknowledged",
    "VREvent_DriverRequestedQuit": "vr-event-driver-requested-quit",
    "VREvent_RestartRequested": "vr-event-restart-requested",
    "VREvent_InvalidateSwapTextureSets": "vr-event-invalidate-swap-texture-sets",
    "VREvent_ChaperoneDataHasChanged": "vr-event-chaperone-data-has-changed",
    "VREvent_ChaperoneUniverseHasChanged": "vr-event-chaperone-universe-has-changed",
    "VREvent_ChaperoneTempDataHasChanged": "vr-event-chaperone-temp-data-has-changed",
    "VREvent_ChaperoneSettingsHaveChanged": "vr-event-chaperone-settings-have-changed",
    "VREvent_SeatedZeroPoseReset": "vr-event-seated-zero-pose-reset",
    "VREvent_ChaperoneFlushCache": "vr-event-chaperone-flush-cache",
    "VREvent_ChaperoneRoomSetupStarting": "vr-event-chaperone-room-setup-starting",
    "VREvent_ChaperoneRoomSetupFinished": "vr-event-chaperone-room-setup-finished",
    "VREvent_StandingZeroPoseReset": "vr-event-standing-zero-pose-reset",
    "VREvent_AudioSettingsHaveChanged": "vr-event-audio-settings-have-changed",
    "VREvent_BackgroundSettingHasChanged": "vr-event-background-setting-has-changed",
    "VREvent_CameraSettingsHaveChanged": "vr-event-camera-settings-have-changed",
    "VREvent_ReprojectionSettingHasChanged": "vr-event-reprojection-setting-has-changed",
    "VREvent_ModelSkinSettingsHaveChanged": "vr-event-model-skin-settings-have-changed",
    "VREvent_EnvironmentSettingsHaveChanged": "vr-event-environment-settings-have-changed",
    "VREvent_PowerSettingsHaveChanged": "vr-event-power-settings-have-changed",
    "VREvent_EnableHomeAppSettingsHaveChanged": "vr-event-enable-home-app-settings-have-changed",
    "VREvent_SteamVRSectionSettingChanged": "vr-event-steam-vr-section-setting-changed",
    "VREvent_LighthouseSectionSettingChanged": "vr-event-lighthouse-section-setting-changed",
    "VREvent_NullSectionSettingChanged": "vr-event-null-section-setting-changed",
    "VREvent_UserInterfaceSectionSettingChanged": "vr-event-user-interface-section-setting-changed",
    "VREvent_NotificationsSectionSettingChanged": "vr-event-notifications-section-setting-changed",
    "VREvent_KeyboardSectionSettingChanged": "vr-event-keyboard-section-setting-changed",
    "VREvent_PerfSectionSettingChanged": "vr-event-perf-section-setting-changed",
    "VREvent_DashboardSectionSettingChanged": "vr-event-dashboard-section-setting-changed",
    "VREvent_WebInterfaceSectionSettingChanged": "vr-event-web-interface-section-setting-changed",
    "VREvent_TrackersSectionSettingChanged": "vr-event-trackers-section-setting-changed",
    "VREvent_LastKnownSectionSettingChanged": "vr-event-last-known-section-setting-changed",
    "VREvent_DismissedWarningsSectionSettingChanged": "vr-event-dismissed-warnings-section-setting-changed",
    "VREvent_GpuSpeedSectionSettingChanged": "vr-event-gpu-speed-section-setting-changed",
    "VREvent_WindowsMRSectionSettingChanged": "vr-event-windows-mr-section-setting-changed",
    "VREvent_OtherSectionSettingChanged": "vr-event-other-section-setting-changed",
    "VREvent_AnyDriverSettingsChanged": "vr-event-any-driver-settings-changed",
    "VREvent_StatusUpdate": "vr-event-status-update",
    "VREvent_WebInterface_InstallDriverCompleted": "vr-event-web-interface-install-driver-completed",
    "VREvent_MCImageUpdated": "vr-event-mc-image-updated",
    "VREvent_FirmwareUpdateStarted": "vr-event-firmware-update-started",
    "VREvent_FirmwareUpdateFinished": "vr-event-firmware-update-finished",
    "VREvent_KeyboardClosed": "vr-event-keyboard-closed",
    "VREvent_KeyboardCharInput": "vr-event-keyboard-char-input",
    "VREvent_KeyboardDone": "vr-event-keyboard-done",
    "VREvent_KeyboardOpened_Global": "vr-event-keyboard-opened-global",
    "VREvent_KeyboardClosed_Global": "vr-event-keyboard-closed-global",
    "VREvent_ApplicationListUpdated": "vr-event-application-list-updated",
    "VREvent_ApplicationMimeTypeLoad": "vr-event-application-mime-type-load",
    "VREvent_ProcessConnected": "vr-event-process-connected",
    "VREvent_ProcessDisconnected": "vr-event-process-disconnected",
    "VREvent_Compositor_ChaperoneBoundsShown": "vr-event-compositor-chaperone-bounds-shown",
    "VREvent_Compositor_ChaperoneBoundsHidden": "vr-event-compositor-chaperone-bounds-hidden",
    "VREvent_Compositor_DisplayDisconnected": "vr-event-compositor-display-disconnected",
    "VREvent_Compositor_DisplayReconnected": "vr-event-compositor-display-reconnected",
    "VREvent_Compositor_HDCPError": "vr-event-compositor-hdcp-error",
    "VREvent_Compositor_ApplicationNotResponding": "vr-event-compositor-application-not-responding",
    "VREvent_Compositor_ApplicationResumed": "vr-event-compositor-application-resumed",
    "VREvent_Compositor_OutOfVideoMemory": "vr-event-compositor-out-of-video-memory",
    "VREvent_Compositor_DisplayModeNotSupported": "vr-event-compositor-display-mode-not-supported",
    "VREvent_Compositor_StageOverrideReady": "vr-event-compositor-stage-override-ready",
    "VREvent_Compositor_RequestDisconnectReconnect": "vr-event-compositor-request-disconnect-reconnect",
    "VREvent_TrackedCamera_StartVideoStream": "vr-event-tracked-camera-start-video-stream",
    "VREvent_TrackedCamera_StopVideoStream": "vr-event-tracked-camera-stop-video-stream",
    "VREvent_TrackedCamera_PauseVideoStream": "vr-event-tracked-camera-pause-video-stream",
    "VREvent_TrackedCamera_ResumeVideoStream": "vr-event-tracked-camera-resume-video-stream",
    "VREvent_TrackedCamera_EditingSurface": "vr-event-tracked-camera-editing-surface",
    "VREvent_PerformanceTest_EnableCapture": "vr-event-performance-test-enable-capture",
    "VREvent_PerformanceTest_DisableCapture": "vr-event-performance-test-disable-capture",
    "VREvent_PerformanceTest_FidelityLevel": "vr-event-performance-test-fidelity-level",
    "VREvent_MessageOverlay_Closed": "vr-event-message-overlay-closed",
    "VREvent_MessageOverlayCloseRequested": "vr-event-message-overlay-close-requested",
    "VREvent_Input_HapticVibration": "vr-event-input-haptic-vibration",
    "VREvent_Input_BindingLoadFailed": "vr-event-input-binding-load-failed",
    "VREvent_Input_BindingLoadSuccessful": "vr-event-input-binding-load-successful",
    "VREvent_Input_ActionManifestReloaded": "vr-event-input-action-manifest-reloaded",
    "VREvent_Input_ActionManifestLoadFailed": "vr-event-input-action-manifest-load-failed",
    "VREvent_Input_ProgressUpdate": "vr-event-input-progress-update",
    "VREvent_Input_TrackerActivated": "vr-event-input-tracker-activated",
    "VREvent_Input_BindingsUpdated": "vr-event-input-bindings-updated",
    "VREvent_Input_BindingSubscriptionChanged": "vr-event-input-binding-subscription-changed",
    "VREvent_SpatialAnchors_PoseUpdated": "vr-event-spatial-anchors-pose-updated",
    "VREvent_SpatialAnchors_DescriptorUpdated": "vr-event-spatial-anchors-descriptor-updated",
    "VREvent_SpatialAnchors_RequestPoseUpdate": "vr-event-spatial-anchors-request-pose-update",
    "VREvent_SpatialAnchors_RequestDescriptorUpdate": "vr-event-spatial-anchors-request-descriptor-update",
    "VREvent_SystemReport_Started": "vr-event-system-report-started",
    "VREvent_Monitor_ShowHeadsetView": "vr-event-monitor-show-headset-view",
    "VREvent_Monitor_HideHeadsetView": "vr-event-monitor-hide-headset-view",
    "VREvent_Audio_SetSpeakersVolume": "vr-event-audio-set-speakers-volume",
    "VREvent_Audio_SetSpeakersMute": "vr-event-audio-set-speakers-mute",
    "VREvent_Audio_SetMicrophoneVolume": "vr-event-audio-set-microphone-volume",
    "VREvent_Audio_SetMicrophoneMute": "vr-event-audio-set-microphone-mute",
    "VREvent_VendorSpecific_Reserved_Start": "vr-event-vendor-specific-reserved-start",
    "VREvent_VendorSpecific_Reserved_End": "vr-event-vendor-specific-reserved-end",
}

VR_EVENT_REVERSE_MAPPING = {v: k for k, v in VR_EVENT_MAPPING.items()}


def normalize_vr_event_name(event_name: str) -> str:
    """
    Normalize VR event names from WebSocket API format to Home Assistant format.

    Args:
        event_name: The event name in WebSocket API format (VREvent_*)

    Returns:
        Normalized event name in Home Assistant format (vr-event-*)
    """
    if not event_name:
        return ""

    if event_name in VR_EVENT_MAPPING:
        return VR_EVENT_MAPPING[event_name]

    return event_name


def denormalize_vr_event_name(event_name: str) -> str:
    """
    Convert Home Assistant format back to WebSocket API format.

    Args:
        event_name: The event name in Home Assistant format (vr-event-*)

    Returns:
        Event name in WebSocket API format (VREvent_*)
    """
    if not event_name:
        return ""

    if event_name in VR_EVENT_REVERSE_MAPPING:
        return VR_EVENT_REVERSE_MAPPING[event_name]

    return event_name
