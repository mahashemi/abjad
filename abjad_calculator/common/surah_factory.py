# ================================================================================
# IMPORTS TO ADD TO surah_factory.py (sorted by chapter number)
# ================================================================================

from ..quran_library import (
    chapter_001_fatiha,
    chapter_002_baqara,
    chapter_003_imran,
    chapter_004_nisa,
    chapter_005_maida,
    chapter_006_anaam,
    chapter_007_araaf,
    chapter_008_anfaal,
    chapter_009_tauba,
    chapter_010_yunus,
    chapter_011_hud,
    chapter_012_yusuf,
    chapter_013_raad,
    chapter_014_ibrahim,
    chapter_015_hijr,
    chapter_016_nahl,
    chapter_017_isra,
    chapter_018_kahf,
    chapter_019_maryam,
    chapter_020_taha,
    chapter_021_ambiya,
    chapter_022_hajj,
    chapter_023_momenoon,
    chapter_024_noor,
    chapter_025_furqaan,
    chapter_026_shoara,
    chapter_027_naml,
    chapter_028_qasas,
    chapter_029_ankaboot,
    chapter_030_room,
    chapter_031_luqman,
    chapter_032_sajdah,
    chapter_033_ahazab,
    chapter_034_saba,
    chapter_035_fatir,
    chapter_036_yaseen,
    chapter_037_saffat,
    chapter_038_suad,
    chapter_039_zumar,
    chapter_040_ghafir,
    chapter_041_fusselat,
    chapter_042_shura,
    chapter_043_zukhruf,
    chapter_044_dukhan,
    chapter_045_jasiya,
    chapter_046_ahqaaf,
    chapter_047_mohammad,
    chapter_048_fath,
    chapter_049_hujraat,
    chapter_050_qaaf,
    chapter_051_zariyat,
    chapter_052_toor,
    chapter_053_najm,
    chapter_054_qamar,
    chapter_055_rahmaan,
    chapter_056_waqia,
    chapter_057_hadeed,
    chapter_058_mujadela,
    chapter_059_hashr,
    chapter_060_mumtahina,
    chapter_061_saff,
    chapter_062_jumah,
    chapter_063_munafeqoon,
    chapter_064_taghabun,
    chapter_065_talaaq,
    chapter_066_tahreem,
    chapter_067_mulk,
    chapter_068_qalam,
    chapter_069_haqa,
    chapter_070_maarej,
    chapter_071_nooh,
    chapter_072_jinn,
    chapter_073_muzammil,
    chapter_074_mudassir,
    chapter_075_qayamat,
    chapter_076_dahr,
    chapter_077_mursalat,
    chapter_078_naba,
    chapter_079_naziyat,
    chapter_080_abas,
    chapter_081_takweer,
    chapter_082_infetaar,
    chapter_083_mutaffefin,
    chapter_084_insheqaq,
    chapter_085_burooj,
    chapter_086_tariq,
    chapter_087_aala,
    chapter_088_ghasheya,
    chapter_089_fajr,
    chapter_090_balad,
    chapter_091_shams,
    chapter_092_layl,
    chapter_093_zuha,
    chapter_094_shara,
    chapter_095_tin,
    chapter_096_alaq,
    chapter_097_qadr,
    chapter_098_bayyinah,
    chapter_099_zilzal,
    chapter_100_aadiyat,
    chapter_101_qaariyah,
    chapter_102_takasur,
    chapter_103_asr,
    chapter_104_humaza,
    chapter_105_fil,
    chapter_106_quraish,
    chapter_107_maun,
    chapter_108_kawthar,
    chapter_109_kafiroon,
    chapter_110_nasr,
    chapter_111_masad,
    chapter_112_ikhlas,
    chapter_113_falaq,
    chapter_114_nas,
)

surah_fatiha_title = "سورة الفاتحة - سورة 1 - عدد آياتها 7".strip()
surah_baqara_title = "سورة البقرة - سورة 2 - عدد آياتها 286".strip()
surah_imran_title = "سورة آل عمران - سورة 3 - عدد آياتها 200".strip()
surah_nisa_title = "سورة النساء - سورة 4 - عدد آياتها 176".strip()
surah_maida_title = "سورة المائدة - سورة 5 - عدد آياتها 120".strip()
surah_anaam_title = "سورة الأنعام - سورة 6 - عدد آياتها 165".strip()
surah_araaf_title = "سورة الأعراف - سورة 7 - عدد آياتها 206".strip()
surah_anfatitle = "سورة الأنفال - سورة 8 - عدد آياتها 75".strip()
surah_tauba_title = "سورة التوبة - سورة 9 - عدد آياتها 129".strip()
surah_yunus_title = "سورة يونس - سورة 10 - عدد آياتها 109".strip()
surah_hud_title = "سورة هود - سورة 11 - عدد آياتها 123".strip()
surah_yusuf_title = "سورة يوسف - سورة 12 - عدد آياتها 111".strip()
surah_raad_title = "سورة الرعد - سورة 13 - عدد آياتها 43".strip()
surah_ibrahim_title = "سورة ابراهيم - سورة 14 - عدد آياتها 52".strip()
surah_hijr_title = "سورة الحجر - سورة 15 - عدد آياتها 99".strip()
surah_nahl_title = "سورة النحل - سورة 16 - عدد آياتها 128".strip()
surah_isra_title = "سورة الإسراء - سورة 17 - عدد آياتها 111".strip()
surah_kahf_title = "سورة الكهف - سورة 18 - عدد آياتها 110".strip()
surah_maryam_title = "سورة مريم - سورة 19 - عدد آياتها 98".strip()
surah_ta_ha_title = "سورة طٰه - سورة 20 - عدد آياتها 135".strip()
surah_ambiya_title = "سورة الأنبياء - سورة 21 - عدد آياتها 112".strip()
surah_hajj_title = "سورة الحج - سورة 22 - عدد آياتها 78".strip()
surah_momenoon_title = "سورة المؤمنون - سورة 23 - عدد آياتها 118".strip()
surah_noor_title = "سورة النور - سورة 24 - عدد آياتها 64".strip()
surah_furqaan_title = "سورة الفرقان - سورة 25 - عدد آياتها 77".strip()
surah_shoara_title = "سورة الشعراء - سورة 26 - عدد آياتها 227".strip()
surah_naml_title = "سورة النمل - سورة 27 - عدد آياتها 93".strip()
surah_qastitle = "سورة القصص - سورة 28 - عدد آياتها 88".strip()
surah_ankaboot_title = "سورة العنكبوت - سورة 29 - عدد آياتها 69".strip()
surah_room_title = "سورة الروم - سورة 30 - عدد آياتها 60".strip()
surah_luqman_title = "سورة لقمان - سورة 31 - عدد آياتها 34".strip()
surah_sajdah_title = "سورة السجدة - سورة 32 - عدد آياتها 30".strip()
surah_ahazab_title = "سورة الأحزاب - سورة 33 - عدد آياتها 73".strip()
surah_saba_title = "سورة سبإ - سورة 34 - عدد آياتها 54".strip()
surah_fatir_title = "سورة فاطر - سورة 35 - عدد آياتها 45".strip()
surah_yaseen_title = "سورة يس - سورة 36 - عدد آياتها 83".strip()
surah_saffat_title = "سورة الصافات - سورة 37 - عدد آياتها 182".strip()
surah_suad_title = "سورة ص - سورة 38 - عدد آياتها 88".strip()
surah_zumar_title = "سورة الزمر - سورة 39 - عدد آياتها 75".strip()
surah_ghafir_title = "سورة غافر - سورة 40 - عدد آياتها 85".strip()
surah_fusselat_title = "سورة فصلت - سورة 41 - عدد آياتها 54".strip()
surah_shura_title = "سورة الشورى - سورة 42 - عدد آياتها 53".strip()
surah_zukhruf_title = "سورة الزخرف - سورة 43 - عدد آياتها 89".strip()
surah_dukhan_title = "سورة الدخان - سورة 44 - عدد آياتها 59".strip()
surah_jasiya_title = "سورة الجاثية - سورة 45 - عدد آياتها 37".strip()
surah_ahqaaf_title = "سورة الأحقاف - سورة 46 - عدد آياتها 35".strip()
surah_mohammad_title = "سورة محمد - سورة 47 - عدد آياتها 38".strip()
surah_fath_title = "سورة الفتح - سورة 48 - عدد آياتها 29".strip()
surah_hujraat_title = "سورة الحجرات - سورة 49 - عدد آياتها 18".strip()
surah_qaaf_title = "سورة ق - سورة 50 - عدد آياتها 45".strip()
surah_zariyat_title = "سورة الذاريات - سورة 51 - عدد آياتها 60".strip()
surah_toor_title = "سورة الطور - سورة 52 - عدد آياتها 49".strip()
surah_najm_title = "سورة النجم - سورة 53 - عدد آياتها 62".strip()
surah_qamar_title = "سورة القمر - سورة 54 - عدد آياتها 55".strip()
surah_rahmaan_title = "سورة الرحمن - سورة 55 - عدد آياتها 78".strip()
surah_waqia_title = "سورة الواقعة - سورة 56 - عدد آياتها 96".strip()
surah_hadeed_title = "سورة الحديد - سورة 57 - عدد آياتها 29".strip()
surah_mujadela_title = "سورة المجادلة - سورة 58 - عدد آياتها 22".strip()
surah_hashr_title = "سورة الحشر - سورة 59 - عدد آياتها 24".strip()
surah_mumtahina_title = "سورة الممتحنة - سورة 60 - عدد آياتها 13".strip()
surah_saff_title = "سورة الصف - سورة 61 - عدد آياتها 14".strip()
surah_jumah_title = "سورة الجمعة - سورة 62 - عدد آياتها 11".strip()
surah_munafeqoon_title = "سورة المنافقون - سورة 63 - عدد آياتها 11".strip()
surah_taghabun_title = "سورة التغابن - سورة 64 - عدد آياتها 18".strip()
surah_talaaq_title = "سورة الطلاق - سورة 65 - عدد آياتها 12".strip()
surah_tahreem_title = "سورة التحريم - سورة 66 - عدد آياتها 12".strip()
surah_mulk_title = "سورة الملك - سورة 67 - عدد آياتها 30".strip()
surah_qalam_title = "سورة القلم - سورة 68 - عدد آياتها 52".strip()
surah_haqa_title = "سورة الحاقة - سورة 69 - عدد آياتها 52".strip()
surah_maarej_title = "سورة المعارج - سورة 70 - عدد آياتها 44".strip()
surah_nooh_title = "سورة نوح - سورة 71 - عدد آياتها 28".strip()
surah_jinn_title = "سورة الجن - سورة 72 - عدد آياتها 28".strip()
surah_muzammil_title = "سورة المزمل - سورة 73 - عدد آياتها 20".strip()
surah_mudassir_title = "سورة المدثر - سورة 74 - عدد آياتها 56".strip()
surah_qayamat_title = "سورة القيامة - سورة 75 - عدد آياتها 40".strip()
surah_dahr_insaan_title = "سورة الانسان - سورة 76 - عدد آياتها 31".strip()
surah_mursalat_title = "سورة المرسلات - سورة 77 - عدد آياتها 50".strip()
surah_naba_title = "سورة النبإ - سورة 78 - عدد آياتها 40".strip()
surah_naziyat_title = "سورة النازعات - سورة 79 - عدد آياتها 46".strip()
surah_abtitle = "سورة عبس - سورة 80 - عدد آياتها 42".strip()
surah_takweer_title = "سورة التكوير - سورة 81 - عدد آياتها 29".strip()
surah_infetaar_title = "سورة الإنفطار - سورة 82 - عدد آياتها 19".strip()
surah_mutaffefin_title = "سورة المطففين - سورة 83 - عدد آياتها 36".strip()
surah_insheqaq_title = "سورة الإنشقاق - سورة 84 - عدد آياتها 25".strip()
surah_burooj_title = "سورة البروج - سورة 85 - عدد آياتها 22".strip()
surah_tariq_title = "سورة الطارق - سورة 86 - عدد آياتها 17".strip()
surah_aala_title = "سورة الأعلى - سورة 87 - عدد آياتها 19".strip()
surah_ghasheya_title = "سورة الغاشية - سورة 88 - عدد آياتها 26".strip()
surah_fajr_title = "سورة الفجر - سورة 89 - عدد آياتها 30".strip()
surah_balad_title = "سورة البلد - سورة 90 - عدد آياتها 20".strip()
surah_shams_title = "سورة الشمس - سورة 91 - عدد آياتها 15".strip()
surah_layl_title = "سورة الليل - سورة 92 - عدد آياتها 21".strip()
surah_zuha_title = "سورة الضحى - سورة 93 - عدد آياتها 11".strip()
surah_shara_title = "سورة الشرح - سورة 94 - عدد آياتها 8".strip()
surah_tin_title = "سورة التين - سورة 95 - عدد آياتها 8".strip()
surah_alaq_title = "سورة العلق - سورة 96 - عدد آياتها 19".strip()
surah_qadr_title = "سورة القدر - سورة 97 - عدد آياتها 5".strip()
surah_bayyinah_title = "سورة البينة - سورة 98 - عدد آياتها 8".strip()
surah_zilztitle = "سورة الزلزلة - سورة 99 - عدد آياتها 8".strip()
surah_aadiyat_title = "سورة العاديات - سورة 100 - عدد آياتها 11".strip()
surah_qaariyah_title = "سورة القارعة - سورة 101 - عدد آياتها 11".strip()
surah_takasur_title = "سورة التكاثر - سورة 102 - عدد آياتها 8".strip()
surah_asr_title = "سورة العصر - سورة 103 - عدد آياتها 3".strip()
surah_humaza_title = "سورة الهمزة - سورة 104 - عدد آياتها 9".strip()
surah_fil_title = "سورة الفيل - سورة 105 - عدد آياتها 5".strip()
surah_quraish_title = "سورة قريش - سورة 106 - عدد آياتها 4".strip()
surah_maun_title = "سورة الماعون - سورة 107 - عدد آياتها 7".strip()
surah_kawthar_title = "سورة الكوثر - سورة 108 - عدد آياتها 3".strip()
surah_kafiroon_title = "سورة الكافرون - سورة 109 - عدد آياتها 6".strip()
surah_nasr_title = "سورة النصر - سورة 110 - عدد آياتها 3".strip()
surah_masad_title = "سورة المسد - سورة 111 - عدد آياتها 5".strip()
surah_ikhltitle = "سورة الإخلاص - سورة 112 - عدد آياتها 4".strip()
surah_falaq_title = "سورة الفلق - سورة 113 - عدد آياتها 5".strip()
surah_ntitle = "سورة الناس - سورة 114 - عدد آياتها 6".strip()


surahs = {
    surah_fatiha_title: chapter_001_fatiha.ayats,
    surah_baqara_title: chapter_002_baqara.ayats,
    surah_imran_title: chapter_003_imran.ayats,
    surah_nisa_title: chapter_004_nisa.ayats,
    surah_maida_title: chapter_005_maida.ayats,
    surah_anaam_title: chapter_006_anaam.ayats,
    surah_araaf_title: chapter_007_araaf.ayats,
    surah_anfatitle: chapter_008_anfaal.ayats,
    surah_tauba_title: chapter_009_tauba.ayats,
    surah_yunus_title: chapter_010_yunus.ayats,
    surah_hud_title: chapter_011_hud.ayats,
    surah_yusuf_title: chapter_012_yusuf.ayats,
    surah_raad_title: chapter_013_raad.ayats,
    surah_ibrahim_title: chapter_014_ibrahim.ayats,
    surah_hijr_title: chapter_015_hijr.ayats,
    surah_nahl_title: chapter_016_nahl.ayats,
    surah_isra_title: chapter_017_isra.ayats,
    surah_kahf_title: chapter_018_kahf.ayats,
    surah_maryam_title: chapter_019_maryam.ayats,
    surah_ta_ha_title: chapter_020_taha.ayats,
    surah_ambiya_title: chapter_021_ambiya.ayats,
    surah_hajj_title: chapter_022_hajj.ayats,
    surah_momenoon_title: chapter_023_momenoon.ayats,
    surah_noor_title: chapter_024_noor.ayats,
    surah_furqaan_title: chapter_025_furqaan.ayats,
    surah_shoara_title: chapter_026_shoara.ayats,
    surah_naml_title: chapter_027_naml.ayats,
    surah_qastitle: chapter_028_qasas.ayats,
    surah_ankaboot_title: chapter_029_ankaboot.ayats,
    surah_room_title: chapter_030_room.ayats,
    surah_luqman_title: chapter_031_luqman.ayats,
    surah_sajdah_title: chapter_032_sajdah.ayats,
    surah_ahazab_title: chapter_033_ahazab.ayats,
    surah_saba_title: chapter_034_saba.ayats,
    surah_fatir_title: chapter_035_fatir.ayats,
    surah_yaseen_title: chapter_036_yaseen.ayats,
    surah_saffat_title: chapter_037_saffat.ayats,
    surah_suad_title: chapter_038_suad.ayats,
    surah_zumar_title: chapter_039_zumar.ayats,
    surah_ghafir_title: chapter_040_ghafir.ayats,
    surah_fusselat_title: chapter_041_fusselat.ayats,
    surah_shura_title: chapter_042_shura.ayats,
    surah_zukhruf_title: chapter_043_zukhruf.ayats,
    surah_dukhan_title: chapter_044_dukhan.ayats,
    surah_jasiya_title: chapter_045_jasiya.ayats,
    surah_ahqaaf_title: chapter_046_ahqaaf.ayats,
    surah_mohammad_title: chapter_047_mohammad.ayats,
    surah_fath_title: chapter_048_fath.ayats,
    surah_hujraat_title: chapter_049_hujraat.ayats,
    surah_qaaf_title: chapter_050_qaaf.ayats,
    surah_zariyat_title: chapter_051_zariyat.ayats,
    surah_toor_title: chapter_052_toor.ayats,
    surah_najm_title: chapter_053_najm.ayats,
    surah_qamar_title: chapter_054_qamar.ayats,
    surah_rahmaan_title: chapter_055_rahmaan.ayats,
    surah_waqia_title: chapter_056_waqia.ayats,
    surah_hadeed_title: chapter_057_hadeed.ayats,
    surah_mujadela_title: chapter_058_mujadela.ayats,
    surah_hashr_title: chapter_059_hashr.ayats,
    surah_mumtahina_title: chapter_060_mumtahina.ayats,
    surah_saff_title: chapter_061_saff.ayats,
    surah_jumah_title: chapter_062_jumah.ayats,
    surah_munafeqoon_title: chapter_063_munafeqoon.ayats,
    surah_taghabun_title: chapter_064_taghabun.ayats,
    surah_talaaq_title: chapter_065_talaaq.ayats,
    surah_tahreem_title: chapter_066_tahreem.ayats,
    surah_mulk_title: chapter_067_mulk.ayats,
    surah_qalam_title: chapter_068_qalam.ayats,
    surah_haqa_title: chapter_069_haqa.ayats,
    surah_maarej_title: chapter_070_maarej.ayats,
    surah_nooh_title: chapter_071_nooh.ayats,
    surah_jinn_title: chapter_072_jinn.ayats,
    surah_muzammil_title: chapter_073_muzammil.ayats,
    surah_mudassir_title: chapter_074_mudassir.ayats,
    surah_qayamat_title: chapter_075_qayamat.ayats,
    surah_dahr_insaan_title: chapter_076_dahr.ayats,
    surah_mursalat_title: chapter_077_mursalat.ayats,
    surah_naba_title: chapter_078_naba.ayats,
    surah_naziyat_title: chapter_079_naziyat.ayats,
    surah_abtitle: chapter_080_abas.ayats,
    surah_takweer_title: chapter_081_takweer.ayats,
    surah_infetaar_title: chapter_082_infetaar.ayats,
    surah_mutaffefin_title: chapter_083_mutaffefin.ayats,
    surah_insheqaq_title: chapter_084_insheqaq.ayats,
    surah_burooj_title: chapter_085_burooj.ayats,
    surah_tariq_title: chapter_086_tariq.ayats,
    surah_aala_title: chapter_087_aala.ayats,
    surah_ghasheya_title: chapter_088_ghasheya.ayats,
    surah_fajr_title: chapter_089_fajr.ayats,
    surah_balad_title: chapter_090_balad.ayats,
    surah_shams_title: chapter_091_shams.ayats,
    surah_layl_title: chapter_092_layl.ayats,
    surah_zuha_title: chapter_093_zuha.ayats,
    surah_shara_title: chapter_094_shara.ayats,
    surah_tin_title: chapter_095_tin.ayats,
    surah_alaq_title: chapter_096_alaq.ayats,
    surah_qadr_title: chapter_097_qadr.ayats,
    surah_bayyinah_title: chapter_098_bayyinah.ayats,
    surah_zilztitle: chapter_099_zilzal.ayats,
    surah_aadiyat_title: chapter_100_aadiyat.ayats,
    surah_qaariyah_title: chapter_101_qaariyah.ayats,
    surah_takasur_title: chapter_102_takasur.ayats,
    surah_asr_title: chapter_103_asr.ayats,
    surah_humaza_title: chapter_104_humaza.ayats,
    surah_fil_title: chapter_105_fil.ayats,
    surah_quraish_title: chapter_106_quraish.ayats,
    surah_maun_title: chapter_107_maun.ayats,
    surah_kawthar_title: chapter_108_kawthar.ayats,
    surah_kafiroon_title: chapter_109_kafiroon.ayats,
    surah_nasr_title: chapter_110_nasr.ayats,
    surah_masad_title: chapter_111_masad.ayats,
    surah_ikhltitle: chapter_112_ikhlas.ayats,
    surah_falaq_title: chapter_113_falaq.ayats,
    surah_ntitle: chapter_114_nas.ayats,
}
