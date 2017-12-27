# -*- coding: utf-8 -*-
import scrapy
import json
import re
import logging
from locations.items import hourstudy

UK_POSTCODES = ['AB10', 'AB11', 'AB12', 'AB15', 'AB16', 'AB21', 'AB22', 'AB23', 'AB24', 'AB25', 'AB99', 'AB13', 'AB14', 'AB30', 'AB31', 'AB32', 'AB33', 'AB34', 'AB35', 'AB36', 'AB37', 'AB38', 'AB39', 'AB41', 'AB42', 'AB43', 'AB44', 'AB45', 'AB51', 'AB52', 'AB53', 'AB54', 'AB55', 'AB56', 'AL1', 'AL2', 'AL3', 'AL4', 'AL5', 'AL6', 'AL7', 'AL7', 'AL8', 'AL9', 'AL10', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20', 'B21', 'B23', 'B24', 'B25', 'B26', 'B27', 'B28', 'B29', 'B30', 'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37', 'B38', 'B40', 'B42', 'B43', 'B44', 'B45', 'B46', 'B47', 'B48', 'B99', 'B49', 'B50', 'B60', 'B61', 'B62', 'B63', 'B64', 'B65', 'B66', 'B67', 'B68', 'B69', 'B70', 'B71', 'B72', 'B73', 'B74', 'B75', 'B76', 'B77', 'B78', 'B79', 'B80', 'B90', 'B91', 'B92', 'B93', 'B94', 'B95', 'B96', 'B97', 'B98', 'BA1', 'BA2', 'BA3', 'BA4', 'BA5', 'BA6', 'BA7', 'BA8', 'BA9', 'BA9', 'BA10', 'BA11', 'BA12', 'BA13', 'BA14', 'BA15', 'BA16', 'BA20', 'BA21', 'BA22', 'BB1', 'BB2', 'BB6', 'BB3', 'BB4', 'BB5', 'BB7', 'BB8', 'BB9', 'BB10', 'BB11', 'BB12', 'BB18', 'BB94', 'BD1', 'BD2', 'BD3', 'BD4', 'BD5', 'BD6', 'BD7', 'BD8', 'BD9', 'BD10', 'BD11', 'BD12', 'BD13', 'BD14', 'BD15', 'BD98', 'BD99', 'BD16', 'BD97', 'BD17', 'BD18', 'BD98', 'BD19', 'BD20', 'BD21', 'BD22', 'BD23', 'BD24', 'BD24', 'BF1', 'BH1', 'BH2', 'BH3', 'BH4', 'BH5', 'BH6', 'BH7', 'BH8', 'BH9', 'BH10', 'BH11', 'BH12', 'BH13', 'BH14', 'BH15', 'BH16', 'BH17', 'BH18', 'BH19', 'BH20', 'BH21', 'BH22', 'BH23', 'BH24', 'BH25', 'BH31', 'BL0', 'BL8', 'BL9', 'BL1', 'BL2', 'BL3', 'BL4', 'BL5', 'BL6', 'BL7', 'BL11', 'BL78', 'BN1', 'BN2', 'BN41', 'BN42', 'BN45', 'BN50', 'BN51', 'BN88', 'BN3', 'BN52', 'BN5', 'BN6', 'BN7', 'BN8', 'BN9', 'BN10', 'BN11', 'BN12', 'BN13', 'BN14', 'BN91', 'BN99', 'BN15', 'BN99', 'BN16', 'BN17', 'BN18', 'BN20', 'BN21', 'BN22', 'BN23', 'BN24', 'BN25', 'BN26', 'BN27', 'BN43', 'BN44', 'BR1', 'BR2', 'BR2', 'BR3', 'BR4', 'BR5', 'BR6', 'BR7', 'BR8', 'BS0', 'BS1', 'BS2', 'BS3', 'BS4', 'BS5', 'BS6', 'BS7', 'BS8', 'BS9', 'BS10', 'BS11', 'BS13', 'BS14', 'BS15', 'BS16', 'BS20', 'BS30', 'BS31', 'BS32', 'BS34', 'BS35', 'BS36', 'BS37', 'BS39', 'BS40', 'BS41', 'BS48', 'BS49', 'BS80', 'BS98', 'BS99', 'BS21', 'BS22', 'BS23', 'BS24', 'BS25', 'BS26', 'BS27', 'BS28', 'BS29', 'BT1', 'BT2', 'BT3', 'BT4', 'BT5', 'BT6', 'BT7', 'BT8', 'BT9', 'BT10', 'BT11', 'BT12', 'BT13', 'BT14', 'BT15', 'BT16', 'BT17', 'BT29', 'BT18', 'BT19', 'BT20', 'BT21', 'BT22', 'BT23', 'BT24', 'BT25', 'BT26', 'BT27', 'BT28', 'BT29', 'BT30', 'BT31', 'BT32', 'BT33', 'BT34', 'BT35', 'BT36', 'BT37', 'BT58', 'BT38', 'BT39', 'BT40', 'BT41', 'BT42', 'BT43', 'BT44', 'BT45', 'BT46', 'BT47', 'BT48', 'BT49', 'BT51', 'BT52', 'BT53', 'BT54', 'BT55', 'BT56', 'BT57', 'BT60', 'BT61', 'BT62', 'BT63', 'BT64', 'BT65', 'BT66', 'BT67', 'BT68', 'BT69', 'BT70', 'BT71', 'BT74', 'BT92', 'BT93', 'BT94', 'BT75', 'BT76', 'BT77', 'BT78', 'BT79', 'BT80', 'BT81', 'BT82', 'CA1', 'CA2', 'CA3', 'CA4', 'CA5', 'CA6', 'CA99', 'CA7', 'CA8', 'CA9', 'CA10', 'CA11', 'CA12', 'CA13', 'CA14', 'CA95', 'CA15', 'CA16', 'CA17', 'CA18', 'CA19', 'CA20', 'CA21', 'CA22', 'CA23', 'CA24', 'CA25', 'CA26', 'CA27', 'CA28', 'CB1', 'CB2', 'CB3', 'CB4', 'CB5', 'CB21', 'CB22', 'CB23', 'CB24', 'CB25', 'CB6', 'CB7', 'CB8', 'CB9', 'CB10', 'CB11', 'CF3', 'CF5', 'CF10', 'CF11', 'CF14', 'CF15', 'CF23', 'CF24', 'CF30', 'CF91', 'CF95', 'CF99', 'CF31', 'CF32', 'CF33', 'CF35', 'CF34', 'CF36', 'CF37', 'CF38', 'CF39', 'CF40', 'CF41', 'CF42', 'CF43', 'CF44', 'CF45', 'CF46', 'CF47', 'CF48', 'CF61', 'CF71', 'CF62', 'CF63', 'CF64', 'CF64', 'CF71', 'CF72', 'CF81', 'CF82', 'CF83', 'CH1', 'CH2', 'CH3', 'CH4', 'CH70', 'CH88', 'CH99', 'CH5', 'CH6', 'CH6', 'CH7', 'CH7', 'CH8', 'CH25', 'CH41', 'CH42', 'CH26', 'CH43', 'CH27', 'CH44', 'CH45', 'CH28', 'CH29', 'CH30', 'CH31', 'CH32', 'CH46', 'CH47', 'CH48', 'CH49', 'CH60', 'CH61', 'CH62', 'CH63', 'CH33', 'CH64', 'CH34', 'CH65', 'CH66', 'CM0', 'CM0', 'CM1', 'CM2', 'CM3', 'CM92', 'CM98', 'CM99', 'CM4', 'CM5', 'CM6', 'CM7', 'CM7', 'CM77', 'CM8', 'CM9', 'CM11', 'CM12', 'CM13', 'CM14', 'CM15', 'CM16', 'CM17', 'CM18', 'CM19', 'CM20', 'CM21', 'CM22', 'CM23', 'CM24', 'CO1', 'CO2', 'CO3', 'CO4', 'CO5', 'CO6', 'CO7', 'CO8', 'CO9', 'CO10', 'CO11', 'CO12', 'CO13', 'CO14', 'CO15', 'CO16', 'CR0', 'CR9', 'CR44', 'CR90', 'CR2', 'CR3', 'CR3', 'CR4', 'CR5', 'CR6', 'CR7', 'CR8', 'CR8', 'CT1', 'CT2', 'CT3', 'CT4', 'CT5', 'CT6', 'CT7', 'CT9', 'CT8', 'CT9', 'CT10', 'CT11', 'CT12', 'CT13', 'CT14', 'CT15', 'CT16', 'CT17', 'CT18', 'CT19', 'CT20', 'CT50', 'CT21', 'CV1', 'CV2', 'CV3', 'CV4', 'CV5', 'CV6', 'CV7', 'CV8', 'CV8', 'CV9', 'CV10', 'CV11', 'CV13', 'CV12', 'CV21', 'CV22', 'CV23', 'CV31', 'CV32', 'CV33', 'CV34', 'CV35', 'CV36', 'CV37', 'CV37', 'CV47', 'CW1', 'CW2', 'CW3', 'CW4', 'CW98', 'CW5', 'CW6', 'CW7', 'CW8', 'CW9', 'CW10', 'CW11', 'CW12', 'DA1', 'DA2', 'DA4', 'DA10', 'DA3', 'DA5', 'DA6', 'DA7', 'DA7', 'DA16', 'DA8', 'DA18', 'DA9', 'DA10', 'DA11', 'DA12', 'DA13', 'DA14', 'DA15', 'DA17', 'DD1', 'DD2', 'DD3', 'DD4', 'DD5', 'DD6', 'DD6', 'DD7', 'DD8', 'DD8', 'DD9', 'DD10', 'DD11', 'DE1', 'DE3', 'DE21', 'DE22', 'DE23', 'DE24', 'DE65', 'DE72', 'DE73', 'DE74', 'DE99', 'DE4', 'DE5', 'DE6', 'DE7', 'DE11', 'DE12', 'DE13', 'DE14', 'DE15', 'DE45', 'DE55', 'DE56', 'DE75', 'DG1', 'DG2', 'DG3', 'DG4', 'DG5', 'DG6', 'DG7', 'DG8', 'DG9', 'DG10', 'DG11', 'DG12', 'DG13', 'DG14', 'DG16', 'DH1', 'DH6', 'DH7', 'DH8', 'DH97', 'DH98', 'DH99', 'DH2', 'DH3', 'DH4', 'DH5', 'DH8', 'DH8', 'DH9', 'DL1', 'DL2', 'DL3', 'DL98', 'DL4', 'DL5', 'DL6', 'DL7', 'DL8', 'DL8', 'DL8', 'DL9', 'DL10', 'DL11', 'DL12', 'DL13', 'DL14', 'DL15', 'DL16', 'DL16', 'DL17', 'DN1', 'DN2', 'DN3', 'DN4', 'DN5', 'DN6', 'DN7', 'DN8', 'DN9', 'DN10', 'DN11', 'DN12', 'DN55', 'DN14', 'DN15', 'DN16', 'DN17', 'DN18', 'DN19', 'DN20', 'DN21', 'DN22', 'DN31', 'DN32', 'DN33', 'DN34', 'DN36', 'DN37', 'DN41', 'DN35', 'DN38', 'DN39', 'DN40', 'DT1', 'DT2', 'DT3', 'DT4', 'DT5', 'DT6', 'DT7', 'DT8', 'DT9', 'DT10', 'DT11', 'DY1', 'DY2', 'DY3', 'DY4', 'DY5', 'DY6', 'DY7', 'DY8', 'DY9', 'DY10', 'DY11', 'DY14', 'DY12', 'DY13', 'E1', 'E1W', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E20', 'E77', 'E98', 'EC1A', 'EC1M', 'EC1N', 'EC1P', 'EC1R', 'EC1V', 'EC1Y', 'EC2A', 'EC2M', 'EC2N', 'EC2P', 'EC2R', 'EC2V', 'EC2Y', 'EC3A', 'EC3M', 'EC3N', 'EC3P', 'EC3R', 'EC3V', 'EC4A', 'EC4M', 'EC4N', 'EC4P', 'EC4R', 'EC4V', 'EC4Y', 'EC50', 'EH1', 'EH2', 'EH3', 'EH4', 'EH5', 'EH6', 'EH7', 'EH8', 'EH9', 'EH10', 'EH11', 'EH12', 'EH13', 'EH14', 'EH15', 'EH16', 'EH17', 'EH91', 'EH95', 'EH99', 'EH14', 'EH14', 'EH14', 'EH18', 'EH19', 'EH20', 'EH21', 'EH22', 'EH23', 'EH24', 'EH25', 'EH26', 'EH27', 'EH28', 'EH29', 'EH30', 'EH31', 'EH32', 'EH32', 'EH33', 'EH34', 'EH35', 'EH36', 'EH37', 'EH38', 'EH39', 'EH40', 'EH41', 'EH42', 'EH43', 'EH44', 'EH45', 'EH46', 'EH47', 'EH48', 'EH49', 'EH51', 'EH52', 'EH53', 'EH54', 'EH55', 'EN1', 'EN2', 'EN3', 'EN4', 'EN5', 'EN6', 'EN7', 'EN8', 'EN77', 'EN9', 'EN10', 'EN11', 'EN11', 'EX1', 'EX2', 'EX3', 'EX4', 'EX5', 'EX6', 'EX7', 'EX8', 'EX9', 'EX10', 'EX11', 'EX12', 'EX13', 'EX14', 'EX15', 'EX16', 'EX17', 'EX18', 'EX19', 'EX20', 'EX20', 'EX21', 'EX22', 'EX23', 'EX24', 'EX31', 'EX32', 'EX33', 'EX34', 'EX34', 'EX35', 'EX35', 'EX36', 'EX37', 'EX38', 'EX39', 'FK1', 'FK2', 'FK3', 'FK4', 'FK5', 'FK6', 'FK7', 'FK8', 'FK9', 'FK10', 'FK10', 'FK11', 'FK12', 'FK13', 'FK14', 'FK15', 'FK16', 'FK17', 'FK18', 'FK19', 'FK20', 'FK21', 'FY0', 'FY1', 'FY2', 'FY3', 'FY4', 'FY5', 'FY6', 'FY7', 'FY8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G9', 'G11', 'G12', 'G13', 'G14', 'G15', 'G20', 'G21', 'G22', 'G23', 'G31', 'G32', 'G33', 'G34', 'G40', 'G41', 'G42', 'G43', 'G44', 'G45', 'G46', 'G51', 'G52', 'G53', 'G58', 'G60', 'G61', 'G62', 'G63', 'G64', 'G65', 'G66', 'G67', 'G68', 'G69', 'G70', 'G71', 'G72', 'G73', 'G74', 'G75', 'G76', 'G77', 'G78', 'G79', 'G90', 'G81', 'G82', 'G83', 'G83', 'G84', 'GL1', 'GL2', 'GL3', 'GL4', 'GL19', 'GL5', 'GL6', 'GL7', 'GL7', 'GL7', 'GL8', 'GL9', 'GL10', 'GL11', 'GL11', 'GL12', 'GL13', 'GL14', 'GL14', 'GL14', 'GL15', 'GL15', 'GL16', 'GL17', 'GL17', 'GL17', 'GL17', 'GL17', 'GL18', 'GL18', 'GL20', 'GL50', 'GL51', 'GL52', 'GL53', 'GL54', 'GL55', 'GL56', 'GU1', 'GU2', 'GU3', 'GU4', 'GU5', 'GU6', 'GU7', 'GU8', 'GU9', 'GU10', 'GU11', 'GU12', 'GU14', 'GU15', 'GU16', 'GU17', 'GU95', 'GU18', 'GU19', 'GU20', 'GU21', 'GU22', 'GU23', 'GU24', 'GU25', 'GU26', 'GU27', 'GU27', 'GU28', 'GU29', 'GU30', 'GU31', 'GU32', 'GU33', 'GU34', 'GU35', 'GU46', 'GU47', 'GU51', 'GU52', 'GY1', 'GY2', 'GY3', 'GY4', 'GY5', 'GY6', 'GY7', 'GY8', 'GY9', 'GY10', 'HA0', 'HA9', 'HA1', 'HA2', 'HA3', 'HA4', 'HA5', 'HA6', 'HA7', 'HA8', 'HD1', 'HD2', 'HD3', 'HD4', 'HD5', 'HD7', 'HD8', 'HD6', 'HD9', 'HG1', 'HG2', 'HG3', 'HG4', 'HG5', 'HP1', 'HP2', 'HP3', 'HP4', 'HP5', 'HP6', 'HP7', 'HP8', 'HP9', 'HP10', 'HP11', 'HP12', 'HP13', 'HP14', 'HP15', 'HP16', 'HP17', 'HP18', 'HP19', 'HP20', 'HP21', 'HP22', 'HP22', 'HP27', 'HP23', 'HR1', 'HR2', 'HR3', 'HR4', 'HR5', 'HR6', 'HR7', 'HR8', 'HR9', 'HS1', 'HS2', 'HS3', 'HS5', 'HS4', 'HS6', 'HS7', 'HS8', 'HS9', 'HU1', 'HU2', 'HU3', 'HU4', 'HU5', 'HU6', 'HU7', 'HU8', 'HU9', 'HU10', 'HU11', 'HU12', 'HU13', 'HU14', 'HU15', 'HU16', 'HU20', 'HU17', 'HU18', 'HU19', 'HX1', 'HX2', 'HX3', 'HX4', 'HX1', 'HX5', 'HX6', 'HX7', 'IG1', 'IG2', 'IG3', 'IG4', 'IG5', 'IG6', 'IG7', 'IG8', 'IG8', 'IG9', 'IG10', 'IG11', 'IM1', 'IM2', 'IM3', 'IM4', 'IM5', 'IM6', 'IM7', 'IM8', 'IM9', 'IM99', 'IP1', 'IP2', 'IP3', 'IP4', 'IP5', 'IP6', 'IP7', 'IP8', 'IP9', 'IP10', 'IP11', 'IP12', 'IP13', 'IP14', 'IP15', 'IP16', 'IP17', 'IP18', 'IP19', 'IP20', 'IP21', 'IP22', 'IP98', 'IP21', 'IP23', 'IP24', 'IP25', 'IP26', 'IP27', 'IP28', 'IP29', 'IP30', 'IP31', 'IP32', 'IP33', 'IV1', 'IV2', 'IV3', 'IV5', 'IV13', 'IV63', 'IV99', 'IV4', 'IV6', 'IV7', 'IV15', 'IV16', 'IV8', 'IV9', 'IV10', 'IV11', 'IV12', 'IV14', 'IV17', 'IV18', 'IV19', 'IV20', 'IV21', 'IV22', 'IV23', 'IV24', 'IV25', 'IV26', 'IV27', 'IV28', 'IV30', 'IV31', 'IV32', 'IV36', 'IV40', 'IV41', 'IV42', 'IV43', 'IV44', 'IV45', 'IV46', 'IV47', 'IV48', 'IV49', 'IV55', 'IV56', 'IV51', 'IV52', 'IV53', 'IV54', 'JE1', 'JE2', 'JE3', 'JE4', 'JE5', 'KA1', 'KA2', 'KA3', 'KA4', 'KA5', 'KA6', 'KA7', 'KA8', 'KA9', 'KA10', 'KA11', 'KA12', 'KA13', 'KA14', 'KA15', 'KA16', 'KA17', 'KA18', 'KA19', 'KA20', 'KA21', 'KA22', 'KA23', 'KA24', 'KA25', 'KA26', 'KA27', 'KA28', 'KA29', 'KA30', 'KT1', 'KT2', 'KT3', 'KT4', 'KT5', 'KT6', 'KT7', 'KT8', 'KT8', 'KT9', 'KT10', 'KT11', 'KT12', 'KT13', 'KT14', 'KT15', 'KT16', 'KT17', 'KT18', 'KT19', 'KT20', 'KT21', 'KT22', 'KT23', 'KT24', 'KW1', 'KW2', 'KW3', 'KW5', 'KW6', 'KW7', 'KW8', 'KW9', 'KW10', 'KW11', 'KW12', 'KW13', 'KW14', 'KW15', 'KW16', 'KW17', 'KY1', 'KY2', 'KY3', 'KY4', 'KY4', 'KY5', 'KY6', 'KY7', 'KY8', 'KY9', 'KY10', 'KY11', 'KY12', 'KY99', 'KY11', 'KY13', 'KY14', 'KY15', 'KY16', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12', 'L13', 'L14', 'L15', 'L16', 'L17', 'L18', 'L19', 'L20', 'L21', 'L22', 'L23', 'L24', 'L25', 'L26', 'L27', 'L28', 'L29', 'L31', 'L32', 'L33', 'L36', 'L37', 'L38', 'L67', 'L68', 'L69', 'L70', 'L71', 'L72', 'L73', 'L74', 'L75', 'L20', 'L30', 'L69', 'L80', 'L34', 'L35', 'L39', 'L40', 'LA1', 'LA2', 'LA3', 'LA4', 'LA5', 'LA6', 'LA7', 'LA8', 'LA9', 'LA10', 'LA11', 'LA12', 'LA13', 'LA14', 'LA14', 'LA15', 'LA16', 'LA17', 'LA18', 'LA19', 'LA20', 'LA21', 'LA22', 'LA23', 'LD1', 'LD2', 'LD3', 'LD4', 'LD5', 'LD6', 'LD7', 'LD8', 'LE1', 'LE2', 'LE3', 'LE4', 'LE5', 'LE6', 'LE7', 'LE8', 'LE9', 'LE19', 'LE21', 'LE41', 'LE55', 'LE87', 'LE94', 'LE95', 'LE10', 'LE11', 'LE12', 'LE13', 'LE14', 'LE15', 'LE16', 'LE17', 'LE18', 'LE65', 'LE67', 'LE67', 'LE67', 'LL11', 'LL12', 'LL13', 'LL14', 'LL15', 'LL16', 'LL17', 'LL18', 'LL18', 'LL19', 'LL20', 'LL21', 'LL22', 'LL23', 'LL24', 'LL25', 'LL26', 'LL27', 'LL28', 'LL29', 'LL30', 'LL31', 'LL32', 'LL31', 'LL33', 'LL34', 'LL35', 'LL36', 'LL37', 'LL38', 'LL39', 'LL40', 'LL41', 'LL42', 'LL43', 'LL44', 'LL45', 'LL46', 'LL47', 'LL48', 'LL49', 'LL51', 'LL52', 'LL53', 'LL54', 'LL55', 'LL56', 'LL57', 'LL58', 'LL59', 'LL60', 'LL61', 'LL62', 'LL63', 'LL64', 'LL77', 'LL65', 'LL66', 'LL67', 'LL68', 'LL69', 'LL70', 'LL71', 'LL72', 'LL73', 'LL74', 'LL75', 'LL76', 'LL77', 'LL78', 'LN1', 'LN2', 'LN3', 'LN4', 'LN5', 'LN6', 'LN7', 'LN8', 'LN9', 'LN10', 'LN11', 'LN12', 'LN13', 'LS1', 'LS2', 'LS3', 'LS4', 'LS5', 'LS6', 'LS7', 'LS8', 'LS9', 'LS10', 'LS11', 'LS12', 'LS13', 'LS14', 'LS15', 'LS16', 'LS17', 'LS18', 'LS19', 'LS20', 'LS25', 'LS26', 'LS27', 'LS88', 'LS98', 'LS99', 'LS21', 'LS22', 'LS23', 'LS24', 'LS28', 'LS29', 'LU1', 'LU2', 'LU3', 'LU4', 'LU5', 'LU6', 'LU7', 'M1', 'M2', 'M3', 'M4', 'M8', 'M9', 'M11', 'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'M19', 'M20', 'M21', 'M22', 'M23', 'M24', 'M25', 'M26', 'M27', 'M28', 'M29', 'M30', 'M31', 'M32', 'M34', 'M35', 'M38', 'M40', 'M41', 'M43', 'M44', 'M45', 'M46', 'M60', 'M61', 'M90', 'M99', 'M3', 'M5', 'M6', 'M7', 'M50', 'M60', 'M33', 'ME1', 'ME2', 'ME3', 'ME4', 'ME5', 'ME6', 'ME20', 'ME6', 'ME6', 'ME19', 'ME7', 'ME8', 'ME9', 'ME10', 'ME11', 'ME12', 'ME13', 'ME14', 'ME15', 'ME16', 'ME17', 'ME18', 'ME99', 'MK1', 'MK2', 'MK3', 'MK4', 'MK5', 'MK6', 'MK7', 'MK8', 'MK9', 'MK10', 'MK11', 'MK12', 'MK13', 'MK14', 'MK15', 'MK17', 'MK19', 'MK77', 'MK16', 'MK18', 'MK40', 'MK41', 'MK42', 'MK43', 'MK44', 'MK45', 'MK46', 'ML1', 'ML2', 'ML3', 'ML4', 'ML5', 'ML6', 'ML7', 'ML8', 'ML9', 'ML10', 'ML11', 'ML12', 'N1', 'N1C', 'N1P', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10', 'N11', 'N12', 'N13', 'N14', 'N15', 'N16', 'N17', 'N18', 'N19', 'N20', 'N21', 'N22', 'N81', 'NE1', 'NE2', 'NE3', 'NE4', 'NE5', 'NE6', 'NE7', 'NE12', 'NE13', 'NE15', 'NE16', 'NE17', 'NE18', 'NE19', 'NE20', 'NE27', 'NE82', 'NE83', 'NE85', 'NE88', 'NE98', 'NE99', 'NE8', 'NE9', 'NE10', 'NE11', 'NE92', 'NE21', 'NE22', 'NE23', 'NE24', 'NE25', 'NE26', 'NE28', 'NE29', 'NE30', 'NE31', 'NE32', 'NE33', 'NE34', 'NE35', 'NE36', 'NE37', 'NE38', 'NE39', 'NE40', 'NE41', 'NE42', 'NE43', 'NE44', 'NE45', 'NE46', 'NE47', 'NE48', 'NE49', 'NE61', 'NE65', 'NE62', 'NE63', 'NE64', 'NE66', 'NE66', 'NE69', 'NE67', 'NE68', 'NE70', 'NE71', 'NG1', 'NG2', 'NG3', 'NG4', 'NG5', 'NG6', 'NG7', 'NG8', 'NG9', 'NG10', 'NG11', 'NG12', 'NG13', 'NG14', 'NG15', 'NG16', 'NG17', 'NG80', 'NG90', 'NG17', 'NG18', 'NG19', 'NG20', 'NG21', 'NG70', 'NG22', 'NG23', 'NG24', 'NG25', 'NG31', 'NG32', 'NG33', 'NG34', 'NN1', 'NN2', 'NN3', 'NN4', 'NN5', 'NN6', 'NN7', 'NN8', 'NN9', 'NN29', 'NN10', 'NN11', 'NN12', 'NN13', 'NN14', 'NN15', 'NN16', 'NN17', 'NN18', 'NP4', 'NP7', 'NP7', 'NP8', 'NP10', 'NP11', 'NP18', 'NP19', 'NP20', 'NP12', 'NP13', 'NP15', 'NP16', 'NP22', 'NP23', 'NP24', 'NP25', 'NP26', 'NP44', 'NR1', 'NR2', 'NR3', 'NR4', 'NR5', 'NR6', 'NR7', 'NR8', 'NR9', 'NR10', 'NR11', 'NR12', 'NR13', 'NR14', 'NR15', 'NR16', 'NR18', 'NR19', 'NR26', 'NR28', 'NR99', 'NR17', 'NR18', 'NR19', 'NR20', 'NR21', 'NR22', 'NR23', 'NR24', 'NR25', 'NR26', 'NR27', 'NR28', 'NR29', 'NR30', 'NR31', 'NR32', 'NR33', 'NR34', 'NR35', 'NW1', 'NW1W', 'NW2', 'NW3', 'NW4', 'NW5', 'NW6', 'NW7', 'NW8', 'NW9', 'NW10', 'NW11', 'NW26', 'OL1', 'OL2', 'OL3', 'OL4', 'OL8', 'OL9', 'OL95', 'OL5', 'OL6', 'OL7', 'OL10', 'OL11', 'OL12', 'OL16', 'OL13', 'OL14', 'OL15', 'OL16', 'OX1', 'OX2', 'OX3', 'OX4', 'OX33', 'OX44', 'OX5', 'OX7', 'OX9', 'OX10', 'OX11', 'OX12', 'OX13', 'OX14', 'OX15', 'OX16', 'OX17', 'OX18', 'OX18', 'OX18', 'OX20', 'OX25', 'OX26', 'OX27', 'OX28', 'OX29', 'OX39', 'OX49', 'PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6', 'PA9', 'PA10', 'PA7', 'PA8', 'PA11', 'PA12', 'PA13', 'PA14', 'PA15', 'PA16', 'PA17', 'PA18', 'PA19', 'PA20', 'PA21', 'PA22', 'PA23', 'PA24', 'PA25', 'PA26', 'PA27', 'PA28', 'PA29', 'PA30', 'PA31', 'PA32', 'PA33', 'PA34', 'PA37', 'PA80', 'PA35', 'PA36', 'PA38', 'PA41', 'PA42', 'PA43', 'PA44', 'PA45', 'PA46', 'PA47', 'PA48', 'PA49', 'PA60', 'PA61', 'PA62', 'PA63', 'PA64', 'PA65', 'PA66', 'PA67', 'PA68', 'PA69', 'PA70', 'PA71', 'PA72', 'PA73', 'PA74', 'PA75', 'PA76', 'PA77', 'PA78', 'PE1', 'PE2', 'PE3', 'PE4', 'PE5', 'PE6', 'PE7', 'PE8', 'PE99', 'PE9', 'PE10', 'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE19', 'PE20', 'PE21', 'PE22', 'PE23', 'PE24', 'PE25', 'PE26', 'PE28', 'PE29', 'PE27', 'PE30', 'PE31', 'PE32', 'PE33', 'PE34', 'PE35', 'PE36', 'PE37', 'PE38', 'PH1', 'PH2', 'PH14', 'PH3', 'PH4', 'PH5', 'PH6', 'PH7', 'PH8', 'PH9', 'PH16', 'PH17', 'PH18', 'PH10', 'PH11', 'PH12', 'PH13', 'PH15', 'PH19', 'PH20', 'PH21', 'PH22', 'PH23', 'PH24', 'PH25', 'PH26', 'PH30', 'PH31', 'PH32', 'PH33', 'PH34', 'PH35', 'PH36', 'PH37', 'PH38', 'PH39', 'PH40', 'PH41', 'PH42', 'PH43', 'PH44', 'PH49', 'PH50', 'PL1', 'PL2', 'PL3', 'PL4', 'PL5', 'PL6', 'PL7', 'PL8', 'PL9', 'PL95', 'PL10', 'PL11', 'PL12', 'PL13', 'PL14', 'PL15', 'PL16', 'PL17', 'PL18', 'PL18', 'PL19', 'PL20', 'PL21', 'PL22', 'PL23', 'PL24', 'PL25', 'PL26', 'PL27', 'PL28', 'PL29', 'PL30', 'PL31', 'PL32', 'PL33', 'PL34', 'PL35', 'PO1', 'PO2', 'PO3', 'PO6', 'PO4', 'PO5', 'PO7', 'PO8', 'PO9', 'PO9', 'PO10', 'PO11', 'PO12', 'PO13', 'PO12', 'PO13', 'PO14', 'PO15', 'PO16', 'PO17', 'PO18', 'PO19', 'PO20', 'PO21', 'PO22', 'PO30', 'PO30', 'PO41', 'PO31', 'PO32', 'PO33', 'PO34', 'PO35', 'PO36', 'PO36', 'PO37', 'PO38', 'PO39', 'PO40', 'PR0', 'PR1', 'PR2', 'PR3', 'PR4', 'PR5', 'PR11', 'PR6', 'PR7', 'PR8', 'PR9', 'PR25', 'PR26', 'RG1', 'RG2', 'RG4', 'RG5', 'RG6', 'RG7', 'RG8', 'RG10', 'RG19', 'RG30', 'RG31', 'RG9', 'RG12', 'RG42', 'RG14', 'RG20', 'RG17', 'RG18', 'RG19', 'RG21', 'RG22', 'RG23', 'RG24', 'RG25', 'RG28', 'RG26', 'RG27', 'RG29', 'RG28', 'RG40', 'RG41', 'RG45', 'RH1', 'RH2', 'RH3', 'RH4', 'RH4', 'RH5', 'RH6', 'RH6', 'RH7', 'RH8', 'RH9', 'RH10', 'RH11', 'RH77', 'RH12', 'RH13', 'RH14', 'RH15', 'RH16', 'RH17', 'RH18', 'RH19', 'RH20', 'RM1', 'RM2', 'RM3', 'RM4', 'RM5', 'RM6', 'RM7', 'RM8', 'RM9', 'RM10', 'RM11', 'RM12', 'RM13', 'RM14', 'RM15', 'RM16', 'RM17', 'RM20', 'RM18', 'RM19', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S17', 'S20', 'S21', 'S25', 'S26', 'S35', 'S36', 'S95', 'S96', 'S97', 'S98', 'S99', 'S18', 'S32', 'S33', 'S40', 'S41', 'S42', 'S43', 'S44', 'S45', 'S49', 'S60', 'S61', 'S62', 'S63', 'S65', 'S66', 'S97', 'S64', 'S70', 'S71', 'S72', 'S73', 'S74', 'S75', 'S80', 'S81', 'SA1', 'SA2', 'SA3', 'SA4', 'SA5', 'SA6', 'SA7', 'SA8', 'SA9', 'SA80', 'SA99', 'SA10', 'SA11', 'SA12', 'SA13', 'SA14', 'SA15', 'SA16', 'SA17', 'SA17', 'SA18', 'SA19', 'SA19', 'SA19', 'SA20', 'SA31', 'SA32', 'SA33', 'SA34', 'SA35', 'SA36', 'SA37', 'SA38', 'SA39', 'SA40', 'SA41', 'SA42', 'SA43', 'SA44', 'SA45', 'SA46', 'SA48', 'SA47', 'SA48', 'SA61', 'SA62', 'SA63', 'SA64', 'SA65', 'SA66', 'SA67', 'SA68', 'SA69', 'SA70', 'SA71', 'SA72', 'SA72', 'SA73', 'SE1', 'SE1P', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8', 'SE9', 'SE10', 'SE11', 'SE12', 'SE13', 'SE14', 'SE15', 'SE16', 'SE17', 'SE18', 'SE19', 'SE20', 'SE21', 'SE22', 'SE23', 'SE24', 'SE25', 'SE26', 'SE27', 'SE28', 'SG1', 'SG2', 'SG3', 'SG4', 'SG5', 'SG6', 'SG6', 'SG7', 'SG8', 'SG9', 'SG10', 'SG11', 'SG12', 'SG13', 'SG14', 'SG15', 'SG16', 'SG17', 'SG18', 'SG19', 'SK1', 'SK2', 'SK3', 'SK4', 'SK5', 'SK6', 'SK7', 'SK12', 'SK8', 'SK9', 'SK9', 'SK10', 'SK11', 'SK13', 'SK14', 'SK15', 'SK16', 'SK17', 'SK22', 'SK23', 'SL0', 'SL1', 'SL2', 'SL3', 'SL95', 'SL4', 'SL5', 'SL6', 'SL60', 'SL7', 'SL8', 'SL9', 'SM1', 'SM2', 'SM3', 'SM4', 'SM5', 'SM6', 'SM7', 'SN1', 'SN2', 'SN3', 'SN4', 'SN5', 'SN6', 'SN25', 'SN26', 'SN38', 'SN99', 'SN7', 'SN8', 'SN9', 'SN10', 'SN11', 'SN12', 'SN13', 'SN15', 'SN14', 'SN15', 'SN16', 'SO14', 'SO15', 'SO16', 'SO17', 'SO18', 'SO19', 'SO30', 'SO31', 'SO32', 'SO40', 'SO45', 'SO52', 'SO97', 'SO20', 'SO21', 'SO22', 'SO23', 'SO25', 'SO24', 'SO40', 'SO43', 'SO41', 'SO42', 'SO50', 'SO53', 'SO51', 'SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'SP7', 'SP8', 'SP9', 'SP10', 'SP11', 'SR1', 'SR2', 'SR3', 'SR4', 'SR5', 'SR6', 'SR9', 'SR7', 'SR8', 'SS0', 'SS1', 'SS1', 'SS2', 'SS3', 'SS22', 'SS99', 'SS4', 'SS5', 'SS6', 'SS7', 'SS8', 'SS9', 'SS11', 'SS12', 'SS13', 'SS14', 'SS15', 'SS16', 'SS17', 'ST1', 'ST2', 'ST3', 'ST4', 'ST6', 'ST7', 'ST8', 'ST9', 'ST10', 'ST11', 'ST12', 'ST5', 'ST55', 'ST13', 'ST14', 'ST15', 'ST16', 'ST17', 'ST18', 'ST19', 'ST20', 'ST21', 'SW1A', 'SW1E', 'SW1H', 'SW1P', 'SW1V', 'SW1W', 'SW1X', 'SW1Y', 'SW2', 'SW3', 'SW4', 'SW5', 'SW6', 'SW7', 'SW8', 'SW9', 'SW10', 'SW11', 'SW12', 'SW13', 'SW14', 'SW15', 'SW16', 'SW17', 'SW18', 'SW19', 'SW20', 'SW95', 'SY1', 'SY2', 'SY3', 'SY4', 'SY5', 'SY99', 'SY6', 'SY7', 'SY7', 'SY7', 'SY8', 'SY9', 'SY10', 'SY11', 'SY12', 'SY13', 'SY14', 'SY15', 'SY16', 'SY17', 'SY17', 'SY18', 'SY19', 'SY20', 'SY21', 'SY22', 'SY22', 'SY22', 'SY22', 'SY22', 'SY23', 'SY23', 'SY23', 'SY24', 'SY24', 'SY24', 'SY25', 'SY25', 'TA1', 'TA2', 'TA3', 'TA4', 'TA5', 'TA6', 'TA7', 'TA8', 'TA9', 'TA10', 'TA11', 'TA12', 'TA13', 'TA14', 'TA15', 'TA16', 'TA17', 'TA18', 'TA19', 'TA20', 'TA21', 'TA22', 'TA23', 'TA24', 'TD1', 'TD2', 'TD3', 'TD4', 'TD5', 'TD6', 'TD7', 'TD8', 'TD9', 'TD9', 'TD10', 'TD11', 'TD12', 'TD12', 'TD12', 'TD13', 'TD14', 'TD15', 'TF1', 'TF2', 'TF3', 'TF4', 'TF5', 'TF6', 'TF7', 'TF8', 'TF9', 'TF10', 'TF11', 'TF12', 'TF13', 'TN1', 'TN2', 'TN3', 'TN4', 'TN2', 'TN5', 'TN6', 'TN7', 'TN8', 'TN9', 'TN10', 'TN11', 'TN12', 'TN13', 'TN14', 'TN15', 'TN16', 'TN17', 'TN18', 'TN19', 'TN20', 'TN21', 'TN22', 'TN23', 'TN24', 'TN25', 'TN26', 'TN27', 'TN28', 'TN29', 'TN30', 'TN31', 'TN32', 'TN33', 'TN34', 'TN35', 'TN36', 'TN37', 'TN38', 'TN39', 'TN40', 'TQ1', 'TQ2', 'TQ3', 'TQ4', 'TQ5', 'TQ6', 'TQ7', 'TQ8', 'TQ9', 'TQ9', 'TQ10', 'TQ11', 'TQ12', 'TQ13', 'TQ14', 'TR1', 'TR2', 'TR3', 'TR4', 'TR5', 'TR6', 'TR7', 'TR8', 'TR9', 'TR10', 'TR11', 'TR12', 'TR13', 'TR14', 'TR15', 'TR16', 'TR17', 'TR18', 'TR19', 'TR20', 'TR21', 'TR22', 'TR23', 'TR24', 'TR25', 'TR26', 'TR27', 'TS1', 'TS2', 'TS3', 'TS4', 'TS5', 'TS6', 'TS7', 'TS8', 'TS9', 'TS10', 'TS11', 'TS12', 'TS13', 'TS14', 'TS15', 'TS16', 'TS17', 'TS18', 'TS19', 'TS20', 'TS21', 'TS22', 'TS23', 'TS24', 'TS25', 'TS26', 'TS27', 'TS28', 'TS29', 'TW1', 'TW2', 'TW3', 'TW4', 'TW5', 'TW6', 'TW7', 'TW8', 'TW9', 'TW10', 'TW11', 'TW12', 'TW13', 'TW14', 'TW15', 'TW16', 'TW17', 'TW18', 'TW19', 'TW20', 'UB1', 'UB2', 'UB3', 'UB3', 'UB4', 'UB5', 'UB5', 'UB6', 'UB18', 'UB7', 'UB8', 'UB8', 'UB9', 'UB10', 'UB11', 'W1A', 'W1B', 'W1C', 'W1D', 'W1F', 'W1G', 'W1H', 'W1J', 'W1K', 'W1S', 'W1T', 'W1U', 'W1W', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14', 'WA1', 'WA2', 'WA3', 'WA4', 'WA5', 'WA55', 'WA6', 'WA7', 'WA8', 'WA88', 'WA9', 'WA10', 'WA11', 'WA12', 'WA13', 'WA14', 'WA15', 'WA16', 'WC1A', 'WC1B', 'WC1E', 'WC1H', 'WC1N', 'WC1R', 'WC1V', 'WC1X', 'WC2A', 'WC2B', 'WC2E', 'WC2H', 'WC2N', 'WC2R', 'WD3', 'WD4', 'WD18', 'WD5', 'WD6', 'WD7', 'WD17', 'WD18', 'WD19', 'WD24', 'WD25', 'WD99', 'WD23', 'WF1', 'WF2', 'WF3', 'WF4', 'WF90', 'WF5', 'WF6', 'WF10', 'WF7', 'WF8', 'WF9', 'WF10', 'WF11', 'WF12', 'WF13', 'WF14', 'WF15', 'WF16', 'WF16', 'WF17', 'WN1', 'WN2', 'WN3', 'WN4', 'WN5', 'WN6', 'WN8', 'WN7', 'WN8', 'WR1', 'WR2', 'WR3', 'WR4', 'WR5', 'WR6', 'WR7', 'WR8', 'WR78', 'WR99', 'WR9', 'WR10', 'WR11', 'WR11', 'WR12', 'WR13', 'WR14', 'WR15', 'WS1', 'WS2', 'WS3', 'WS4', 'WS5', 'WS6', 'WS8', 'WS9', 'WS7', 'WS10', 'WS11', 'WS12', 'WS13', 'WS14', 'WS15', 'WV1', 'WV2', 'WV3', 'WV4', 'WV5', 'WV6', 'WV7', 'WV8', 'WV9', 'WV10', 'WV11', 'WV98', 'WV1', 'WV12', 'WV13', 'WV14', 'WV15', 'WV16', 'YO1', 'YO10', 'YO19', 'YO23', 'YO24', 'YO26', 'YO30', 'YO31', 'YO32', 'YO41', 'YO42', 'YO43', 'YO51', 'YO60', 'YO61', 'YO62', 'YO90', 'YO91', 'YO7', 'YO8', 'YO11', 'YO12', 'YO13', 'YO14', 'YO15', 'YO16', 'YO17', 'YO18', 'YO21', 'YO22', 'YO25', 'ZE1', 'ZE2', 'ZE3']

URL = 'https://www.spar.co.uk/umbraco/api/storesearch/searchstores?maxResults=1000&radius=25&startNodeId=1053&location=%s'
HEADERS = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.spar.co.uk/store-locator',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

class SparSpider(scrapy.Spider):
    """ The UK Spar api disregards modified maxResults arguments, and only allows 5 results per request.
        Therefore, this spider works by sending a large number of requests, each having a different
        postcode.
    """ 
    name = "spar"
    allowed_domains = ["spar.co.uk"]
    download_delay = 0.5

    def start_requests(self):
        for postcode in UK_POSTCODES:
            yield scrapy.http.FormRequest(
                url=URL % (postcode), 
                headers=HEADERS, 
                callback=self.parse
            )

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        stores = data['locations']
        if stores:
            for store in stores:
                properties = {
                    'ref': store.get('code'),
                    'name': store.get('name'),
                    'addr_full': store.get('address'),
                    'lat': store.get('lat'),
                    'lon': store.get('lng'),
                    'phone': store.get('telephone'),
                }
                if store.get('url'):
                    properties['website'] = 'https://spar.co.uk' + store.get('url')

                yield hourstudy(**properties)
