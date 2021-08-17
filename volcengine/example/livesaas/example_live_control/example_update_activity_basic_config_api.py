from volcengine.livesaas.LivesaasService import LivesaasService

if __name__ == '__main__':
    livesaasService = LivesaasService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    livesaasService.set_ak('AK')
    livesaasService.set_sk('SK')

    body = {
        "ActivityId": 1,
        "Name": "test",
        "LiveTime": 1628130120,
        "IsCoverImageEnable": 1,
        "CoverImageUrl": "",
        "CoverImageUrlDefault": "",
        "IsPcBackImageEnable": 1,
        "PcBackImageUrl": "",
        "PcBackImageUrlDefault": "",
        "IsMobileBackImageEnable": 1,
        "MobileBackImageUrl": "",
        "MobileBackImageUrlDefault": "",
        "IsPreviewVideoEnable": 0,
        "PreviewVideoUrl": "",
        "PreviewVideoVid": "",
        "PreviewVideoVidDefault": "",
        "IsPeopleCountEnable": 0,
        "IsHeaderImageEnable": 0,
        "HeaderImageUrl": "",
        "IsWatermarkImageEnable": 0,
        "WatermarkImageUrl": "",
        "IsThumbUpEnable": 0,
        "ThumbUpUrl": "",
        "ThumbUpUrlDefault": "",
        "IsShareIconEnable": 0,
        "ShareIconUrl": "",
        "ShareIconUrlDefault": "",
        "IsCommentTranslateEnable": 0,
        "Announcement": "",
        "IsAnnouncementEnable": 0,
        "BackgroundColor": "",
        "InteractionColor": "",
        "FontColor": "",
        "ColorThemeIndex": "",
        "IsPCHeaderImageEnable": 0,
        "PCHeaderImageUrl": "",
        "IsCountdownEnable": 0,
        "IsAutoStartEnable": 0,
        "IsPageLimitEnable": 0,
        "PageLimitType": "",
        "IsLanguageEnable": 0,
        "LanguageType": [],
        "SiteTags": [{
            "Index": 1,
            "Value": "",
            "DbIndex": 1,
            "Show": 0,
            "Name": ""
        }, {
            "Index": 2,
            "Value": "",
            "DbIndex": 3,
            "Show": 0,
            "Name": ""
        }, {
            "Index": 3,
            "Value": "",
            "DbIndex": 2,
            "Show": 0,
            "Name": ""
        }],
        "AutoStartType": 0,
        "IsPlayerTopEnable": 0,
        "PlayerTopType": [],
        "IsReplayAutoOnlineEnable": 1,
        "PreviewVideoId": 0,
        "AccountId": 0,
        "PreviewVideoReviewStatus": 0,
        "DefaultSubtitleLanguage": "",
        "SourceSubtitleLanguage": "",
        "OpenLiveAvextractorTask": 0,
        "IsTimeShift": 0,
        "PreviewVideoCoverImage": "",
        "PreviewVideoMediaName": "",
        "IsPreviewPromptEnable": 1,
        "PreviewPrompt": "直播即将开始，请稍候",
        "IsReservationEnable": 0,
        "ReservationTime": 0,
        "ReservationText": "",
        "WatermarkPosition": 0,
        "IsReplayBulletChat": 0,
        "PresenterChatColor": "",
        "IsLiveBulletChat": 0,
        "IsBackgroundBlur": 0,
        "FeedbackMessage": "",
        "IsFeedbackEnable": 0,
        "IsThumbUpNumberEnable": 1
    }

    resp = livesaasService.update_activity_basic_config_api(body)
    # resp = await livesaasService.async_update_activity_basic_config_api(body)
    print(resp)
