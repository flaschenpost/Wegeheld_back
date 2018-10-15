-- MySQL dump 10.13  Distrib 5.6.38, for Linux (x86_64)
--
-- Host: wegeheldinstance.c18w3andlhxe.eu-central-1.rds.amazonaws.com    Database: held
-- ------------------------------------------------------
-- Server version	5.6.37-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `backend_layout`
--

DROP TABLE IF EXISTS `backend_layout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backend_layout` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL DEFAULT '0',
  `t3ver_oid` int(11) NOT NULL DEFAULT '0',
  `t3ver_id` int(11) NOT NULL DEFAULT '0',
  `t3ver_wsid` int(11) NOT NULL DEFAULT '0',
  `t3ver_label` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `t3ver_state` tinyint(4) NOT NULL DEFAULT '0',
  `t3ver_stage` int(11) NOT NULL DEFAULT '0',
  `t3ver_count` int(11) NOT NULL DEFAULT '0',
  `t3ver_tstamp` int(11) NOT NULL DEFAULT '0',
  `t3ver_move_id` int(11) NOT NULL DEFAULT '0',
  `t3_origuid` int(11) NOT NULL DEFAULT '0',
  `tstamp` int(11) unsigned NOT NULL DEFAULT '0',
  `crdate` int(11) unsigned NOT NULL DEFAULT '0',
  `cruser_id` int(11) unsigned NOT NULL DEFAULT '0',
  `hidden` tinyint(4) unsigned NOT NULL DEFAULT '0',
  `deleted` tinyint(4) NOT NULL DEFAULT '0',
  `sorting` int(11) unsigned NOT NULL DEFAULT '0',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `description` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `config` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `parent` (`pid`),
  KEY `t3ver_oid` (`t3ver_oid`,`t3ver_wsid`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bak_2018_04_27`
--

DROP TABLE IF EXISTS `bak_2018_04_27`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bak_2018_04_27` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `longitude` decimal(11,6) NOT NULL,
  `latitude` decimal(11,6) NOT NULL,
  `date` datetime(6) NOT NULL,
  `photos` int(11) NOT NULL,
  `free_text` varchar(155) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `action_id` int(11) NOT NULL,
  `address_id` int(11) NOT NULL,
  `car_id` int(11) DEFAULT NULL,
  `funny_saying_id` int(11) DEFAULT NULL,
  `offense_id` int(11) NOT NULL,
  `reporter_id` int(11) NOT NULL,
  `tweet` varchar(115) COLLATE utf8mb4_unicode_ci NOT NULL,
  `obstruction_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `wegeheld_report_action_id_bcda63ba_fk_wegeheld_action_id` (`action_id`),
  KEY `wegeheld_report_address_id_489b4072_fk_wegeheld_address_id` (`address_id`),
  KEY `wegeheld_report_car_id_2c9f92e6_fk_wegeheld_car_id` (`car_id`),
  KEY `wegeheld_report_funny_saying_id_09eeebd3_fk_wegeheld_` (`funny_saying_id`),
  KEY `wegeheld_report_offense_id_c27e03a0_fk_wegeheld_offense_id` (`offense_id`),
  KEY `wegeheld_report_reporter_id_64f1d1d9_fk_wegeheld_reporter_id` (`reporter_id`),
  KEY `wegeheld_report_obstruction_id_8809481e_fk_wegeheld_` (`obstruction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53083 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bck_django_migrations`
--

DROP TABLE IF EXISTS `bck_django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bck_django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `be_groups`
--

DROP TABLE IF EXISTS `be_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `be_groups` (
  `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) unsigned NOT NULL DEFAULT '0',
  `tstamp` int(11) unsigned NOT NULL DEFAULT '0',
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `non_exclude_fields` mediumtext COLLATE utf8mb4_unicode_ci,
  `explicit_allowdeny` mediumtext COLLATE utf8mb4_unicode_ci,
  `allowed_languages` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `custom_options` mediumtext COLLATE utf8mb4_unicode_ci,
  `db_mountpoints` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `pagetypes_select` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `tables_select` mediumtext COLLATE utf8mb4_unicode_ci,
  `tables_modify` mediumtext COLLATE utf8mb4_unicode_ci,
  `crdate` int(11) unsigned NOT NULL DEFAULT '0',
  `cruser_id` int(11) unsigned NOT NULL DEFAULT '0',
  `groupMods` mediumtext COLLATE utf8mb4_unicode_ci,
  `file_mountpoints` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `fileoper_perms` tinyint(4) NOT NULL DEFAULT '0',
  `hidden` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `inc_access_lists` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `description` mediumtext COLLATE utf8mb4_unicode_ci,
  `lockToDomain` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `TSconfig` mediumtext COLLATE utf8mb4_unicode_ci,
  `subgroup` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `hide_in_lists` tinyint(4) NOT NULL DEFAULT '0',
  `workspace_perms` tinyint(3) NOT NULL DEFAULT '1',
  `tt_news_categorymounts` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`uid`),
  KEY `parent` (`pid`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `be_sessions`
--

DROP TABLE IF EXISTS `be_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `be_sessions` (
  `ses_id` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `ses_name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `ses_iplock` varchar(39) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `ses_hashlock` int(11) NOT NULL DEFAULT '0',
  `ses_userid` int(11) unsigned NOT NULL DEFAULT '0',
  `ses_tstamp` int(11) unsigned NOT NULL DEFAULT '0',
  `ses_data` longtext COLLATE utf8mb4_unicode_ci,
  `ses_backuserid` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ses_id`,`ses_name`),
  KEY `ses_tstamp` (`ses_tstamp`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `be_users`
--

DROP TABLE IF EXISTS `be_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `be_users` (
  `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) unsigned NOT NULL DEFAULT '0',
  `tstamp` int(11) unsigned NOT NULL DEFAULT '0',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `password` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `admin` tinyint(4) unsigned NOT NULL DEFAULT '0',
  `usergroup` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `disable` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `starttime` int(11) unsigned NOT NULL DEFAULT '0',
  `endtime` int(11) unsigned NOT NULL DEFAULT '0',
  `lang` char(2) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `email` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `db_mountpoints` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `options` tinyint(4) unsigned NOT NULL DEFAULT '0',
  `crdate` int(11) unsigned NOT NULL DEFAULT '0',
  `cruser_id` int(11) unsigned NOT NULL DEFAULT '0',
  `realName` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `userMods` mediumtext COLLATE utf8mb4_unicode_ci,
  `allowed_languages` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `uc` longtext COLLATE utf8mb4_unicode_ci,
  `file_mountpoints` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `fileoper_perms` tinyint(4) NOT NULL DEFAULT '0',
  `workspace_perms` tinyint(3) NOT NULL DEFAULT '1',
  `lockToDomain` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `disableIPlock` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `deleted` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `TSconfig` mediumtext COLLATE utf8mb4_unicode_ci,
  `lastlogin` int(10) unsigned NOT NULL DEFAULT '0',
  `createdByAction` int(11) NOT NULL DEFAULT '0',
  `usergroup_cached_list` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `workspace_id` int(11) NOT NULL DEFAULT '0',
  `workspace_preview` tinyint(3) NOT NULL DEFAULT '1',
  `tt_news_categorymounts` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`uid`),
  KEY `parent` (`pid`),
  KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cache_imagesizes`
--

DROP TABLE IF EXISTS `cache_imagesizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cache_imagesizes` (
  `md5hash` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `md5filename` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `tstamp` int(11) NOT NULL DEFAULT '0',
  `filename` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `imagewidth` mediumint(11) unsigned NOT NULL DEFAULT '0',
  `imageheight` mediumint(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`md5filename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office_20180404`
--

DROP TABLE IF EXISTS `office_20180404`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `office_20180404` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `postalcode` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `postalcode` (`postalcode`(60))
) ENGINE=InnoDB AUTO_INCREMENT=2972 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `old_office`
--

DROP TABLE IF EXISTS `old_office`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `old_office` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `postalcode` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2972 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tmp_rep`
--

DROP TABLE IF EXISTS `tmp_rep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmp_rep` (
  `id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_action`
--

DROP TABLE IF EXISTS `wegeheld_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_map` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name_app` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_address`
--

DROP TABLE IF EXISTS `wegeheld_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `streetnumber` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `street_id` int(11) NOT NULL,
  `town_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wegeheld_address_street_id_7f7a5d40_fk_wegeheld_street_id` (`street_id`),
  KEY `wegeheld_address_town_id_c93f21eb_fk_wegeheld_town_id` (`town_id`),
  CONSTRAINT `wegeheld_address_street_id_7f7a5d40_fk_wegeheld_street_id` FOREIGN KEY (`street_id`) REFERENCES `wegeheld_street` (`id`),
  CONSTRAINT `wegeheld_address_town_id_c93f21eb_fk_wegeheld_town_id` FOREIGN KEY (`town_id`) REFERENCES `wegeheld_town` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38822 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_car`
--

DROP TABLE IF EXISTS `wegeheld_car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_car` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `licenseplate` varchar(70) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `brand_id` int(11) NOT NULL,
  `color_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wegeheld_car_brand_id_9db2f90d_fk_wegeheld_carbrand_id` (`brand_id`),
  KEY `wegeheld_car_color_id_3810b540_fk_wegeheld_carcolor_id` (`color_id`),
  CONSTRAINT `wegeheld_car_brand_id_9db2f90d_fk_wegeheld_carbrand_id` FOREIGN KEY (`brand_id`) REFERENCES `wegeheld_carbrand` (`id`),
  CONSTRAINT `wegeheld_car_color_id_3810b540_fk_wegeheld_carcolor_id` FOREIGN KEY (`color_id`) REFERENCES `wegeheld_carcolor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31335 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_carbrand`
--

DROP TABLE IF EXISTS `wegeheld_carbrand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_carbrand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_carcolor`
--

DROP TABLE IF EXISTS `wegeheld_carcolor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_carcolor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `hexValue` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_emailtext`
--

DROP TABLE IF EXISTS `wegeheld_emailtext`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_emailtext` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `postalcode` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hidden` tinyint(1) NOT NULL,
  `template` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `offense_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `wegeheld_emailtext_offense_id_57cc054a_fk_wegeheld_offense_id` (`offense_id`),
  CONSTRAINT `wegeheld_emailtext_offense_id_57cc054a_fk_wegeheld_offense_id` FOREIGN KEY (`offense_id`) REFERENCES `wegeheld_offense` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_funnysaying`
--

DROP TABLE IF EXISTS `wegeheld_funnysaying`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_funnysaying` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `valid_offenses_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `wegeheld_funnysaying_valid_offenses_id_89ea1ece_fk_wegeheld_` (`valid_offenses_id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_obstruction`
--

DROP TABLE IF EXISTS `wegeheld_obstruction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_obstruction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(190) NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `remark` varchar(190) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_offense`
--

DROP TABLE IF EXISTS `wegeheld_offense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_offense` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(90) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fee` decimal(7,2) NOT NULL,
  `icon` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_photo`
--

DROP TABLE IF EXISTS `wegeheld_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_photo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(90) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `report_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wegeheld_photo_report_id_8bdb769f_fk_wegeheld_report_id` (`report_id`),
  CONSTRAINT `wegeheld_photo_report_id_8bdb769f_fk_wegeheld_report_id` FOREIGN KEY (`report_id`) REFERENCES `wegeheld_report` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53795 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_publicaffairsoffice`
--

DROP TABLE IF EXISTS `wegeheld_publicaffairsoffice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_publicaffairsoffice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `postalcode` varchar(55) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `postalcode` (`postalcode`),
  UNIQUE KEY `wegeheld_publicaffairsoffice_postalcode_b718fefa_uniq` (`postalcode`)
) ENGINE=InnoDB AUTO_INCREMENT=3016 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_report`
--

DROP TABLE IF EXISTS `wegeheld_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `longitude` decimal(11,6) NOT NULL,
  `latitude` decimal(11,6) NOT NULL,
  `date` datetime(6) NOT NULL,
  `photos` int(11) NOT NULL,
  `free_text` varchar(155) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `action_id` int(11) NOT NULL,
  `address_id` int(11) NOT NULL,
  `car_id` int(11) DEFAULT NULL,
  `funny_saying_id` int(11) DEFAULT NULL,
  `offense_id` int(11) NOT NULL,
  `reporter_id` int(11) NOT NULL,
  `tweet` varchar(115) COLLATE utf8mb4_unicode_ci NOT NULL,
  `obstruction_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `wegeheld_report_action_id_bcda63ba_fk_wegeheld_action_id` (`action_id`),
  KEY `wegeheld_report_address_id_489b4072_fk_wegeheld_address_id` (`address_id`),
  KEY `wegeheld_report_car_id_2c9f92e6_fk_wegeheld_car_id` (`car_id`),
  KEY `wegeheld_report_funny_saying_id_09eeebd3_fk_wegeheld_` (`funny_saying_id`),
  KEY `wegeheld_report_offense_id_c27e03a0_fk_wegeheld_offense_id` (`offense_id`),
  KEY `wegeheld_report_reporter_id_64f1d1d9_fk_wegeheld_reporter_id` (`reporter_id`),
  KEY `wegeheld_report_obstruction_id_8809481e_fk_wegeheld_` (`obstruction_id`),
  CONSTRAINT `wegeheld_report_action_id_bcda63ba_fk_wegeheld_action_id` FOREIGN KEY (`action_id`) REFERENCES `wegeheld_action` (`id`),
  CONSTRAINT `wegeheld_report_address_id_489b4072_fk_wegeheld_address_id` FOREIGN KEY (`address_id`) REFERENCES `wegeheld_address` (`id`),
  CONSTRAINT `wegeheld_report_car_id_2c9f92e6_fk_wegeheld_car_id` FOREIGN KEY (`car_id`) REFERENCES `wegeheld_car` (`id`),
  CONSTRAINT `wegeheld_report_obstruction_id_8809481e_fk_wegeheld_` FOREIGN KEY (`obstruction_id`) REFERENCES `wegeheld_obstruction` (`id`),
  CONSTRAINT `wegeheld_report_offense_id_c27e03a0_fk_wegeheld_offense_id` FOREIGN KEY (`offense_id`) REFERENCES `wegeheld_offense` (`id`),
  CONSTRAINT `wegeheld_report_reporter_id_64f1d1d9_fk_wegeheld_reporter_id` FOREIGN KEY (`reporter_id`) REFERENCES `wegeheld_reporter` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80218 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_reporter`
--

DROP TABLE IF EXISTS `wegeheld_reporter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_reporter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nickname` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `zip` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `list_position` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `authkey` char(66) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35744 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_street`
--

DROP TABLE IF EXISTS `wegeheld_street`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_street` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `town_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `wegeheld_street_town_id_29568cd0_fk_wegeheld_town_id` (`town_id`),
  CONSTRAINT `wegeheld_street_town_id_29568cd0_fk_wegeheld_town_id` FOREIGN KEY (`town_id`) REFERENCES `wegeheld_town` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20779 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wegeheld_town`
--

DROP TABLE IF EXISTS `wegeheld_town`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wegeheld_town` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tmstmp` datetime(6) NOT NULL,
  `crdate` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `postalcode` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4226 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-14 23:38:36
