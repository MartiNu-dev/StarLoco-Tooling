/*
 Navicat MariaDB Data Transfer

 Source Server         : StarLoco
 Source Server Type    : MariaDB
 Source Server Version : 100322 (10.3.22-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : game

 Target Server Type    : MariaDB
 Target Server Version : 100322 (10.3.22-MariaDB)
 File Encoding         : 65001

 Date: 08/05/2023 23:46:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
use starloco_game;

-- ----------------------------
-- Table structure for animations
-- ----------------------------
DROP TABLE IF EXISTS `animations`;
CREATE TABLE `animations`  (
  `guid` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) NOT NULL DEFAULT 0,
  `nom` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  `area` int(11) NOT NULL DEFAULT 0,
  `action` int(11) NOT NULL DEFAULT 0,
  `size` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`guid`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 459 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for area_data
-- ----------------------------
DROP TABLE IF EXISTS `area_data`;
CREATE TABLE `area_data`  (
  `id` int(11) NOT NULL,
  `alignement` int(11) NOT NULL DEFAULT -1,
  `Prisme` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Fixed;


-- ----------------------------
-- Table structure for auctions
-- ----------------------------
DROP TABLE IF EXISTS `auctions`;
CREATE TABLE `auctions`  (
  `price` int(11) NOT NULL,
  `owner` int(11) NOT NULL,
  `object` int(11) NOT NULL,
  `retry` tinyint(1) NOT NULL,
  PRIMARY KEY (`object`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Fixed;


-- ----------------------------
-- Table structure for bandits
-- ----------------------------
DROP TABLE IF EXISTS `bandits`;
CREATE TABLE `bandits`  (
  `mobs` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `maps` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `time` bigint(20) NOT NULL DEFAULT 0,
  PRIMARY KEY (`time`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for banks
-- ----------------------------
DROP TABLE IF EXISTS `banks`;
CREATE TABLE `banks`  (
  `id` int(11) UNSIGNED ZEROFILL NOT NULL,
  `kamas` int(11) NOT NULL DEFAULT 0,
  `items` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for challenge
-- ----------------------------
DROP TABLE IF EXISTS `challenge`;
CREATE TABLE `challenge`  (
  `id` int(11) NOT NULL,
  `nom` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `gainXp` int(11) NOT NULL DEFAULT 0,
  `gainDrop` int(11) NOT NULL DEFAULT 0,
  `gainParMob` int(11) NOT NULL DEFAULT 5,
  `conditions` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for coffres
-- ----------------------------
DROP TABLE IF EXISTS `coffres`;
CREATE TABLE `coffres`  (
  `id` int(11) NOT NULL,
  `object` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `kamas` int(11) NOT NULL,
  `key` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '-',
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for crafts
-- ----------------------------
DROP TABLE IF EXISTS `crafts`;
CREATE TABLE `crafts`  (
  `id` int(11) NOT NULL,
  `craft` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  UNIQUE INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for donjons
-- ----------------------------
DROP TABLE IF EXISTS `donjons`;
CREATE TABLE `donjons`  (
  `map` int(11) NOT NULL DEFAULT 0,
  `npc` int(11) NOT NULL DEFAULT 0,
  `key` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `donjon` tinytext CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`map`, `npc`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for drops
-- ----------------------------
DROP TABLE IF EXISTS `drops`;
CREATE TABLE `drops`  (
  `monsterName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `monsterId` int(10) UNSIGNED NOT NULL,
  `objectName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `objectId` int(10) UNSIGNED NOT NULL,
  `percentGrade1` decimal(6, 3) UNSIGNED NOT NULL,
  `percentGrade2` decimal(6, 3) UNSIGNED NOT NULL,
  `percentGrade3` decimal(6, 3) UNSIGNED NOT NULL,
  `percentGrade4` decimal(6, 3) UNSIGNED NOT NULL,
  `percentGrade5` decimal(6, 3) UNSIGNED NOT NULL,
  `ceil` smallint(5) UNSIGNED NOT NULL COMMENT 'Prospection ceil',
  `action` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1',
  `level` int(11) NOT NULL DEFAULT -1,
  PRIMARY KEY (`monsterId`, `objectId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for endfight_action
-- ----------------------------
DROP TABLE IF EXISTS `endfight_action`;
CREATE TABLE `endfight_action`  (
  `map` int(11) NOT NULL,
  `fighttype` int(11) NOT NULL,
  `action` int(11) NOT NULL,
  `args` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cond` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`map`) USING BTREE,
  INDEX `map`(`map`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for extra_monster
-- ----------------------------
DROP TABLE IF EXISTS `extra_monster`;
CREATE TABLE `extra_monster`  (
  `idMob` int(11) NOT NULL,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `superArea` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `subArea` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `chances` int(11) NOT NULL DEFAULT -1,
  PRIMARY KEY (`idMob`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for full_morphs
-- ----------------------------
DROP TABLE IF EXISTS `full_morphs`;
CREATE TABLE `full_morphs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gfxId` int(11) NOT NULL,
  `spells` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `args` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 27 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for gifts
-- ----------------------------
DROP TABLE IF EXISTS `gifts`;
CREATE TABLE `gifts`  (
  `id` int(11) NOT NULL,
  `objects` varchar(1028) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for guild_members
-- ----------------------------
DROP TABLE IF EXISTS `guild_members`;
CREATE TABLE `guild_members`  (
  `guid` int(11) NOT NULL,
  `guild` int(11) NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `level` int(11) NOT NULL,
  `gfxid` int(11) NOT NULL,
  `rank` int(11) NOT NULL,
  `xpdone` bigint(20) NOT NULL,
  `pxp` int(11) NOT NULL,
  `rights` int(11) NOT NULL,
  `align` tinyint(4) NOT NULL,
  `lastConnection` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  UNIQUE INDEX `guid`(`guid`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for hdvs
-- ----------------------------
DROP TABLE IF EXISTS `hdvs`;
CREATE TABLE `hdvs`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `map` int(11) NOT NULL,
  `categories` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sellTaxe` double NOT NULL DEFAULT 1,
  `lvlMax` int(11) NOT NULL DEFAULT 2000,
  `accountItem` int(11) NOT NULL DEFAULT 20,
  `sellTime` int(11) NOT NULL DEFAULT 350,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 101 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for hdvs_items
-- ----------------------------
DROP TABLE IF EXISTS `hdvs_items`;
CREATE TABLE `hdvs_items`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `map` int(11) NOT NULL,
  `ownerGuid` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `sellDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'rien',
  `itemID` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for heroic_mobs_groups
-- ----------------------------
DROP TABLE IF EXISTS `heroic_mobs_groups`;
CREATE TABLE `heroic_mobs_groups`  (
  `id` bigint(20) NOT NULL,
  `map` int(11) NOT NULL,
  `cell` int(11) NOT NULL,
  `group` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `objects` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stars` int(11) NOT NULL
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for heroic_mobs_groups_fix
-- ----------------------------
DROP TABLE IF EXISTS `heroic_mobs_groups_fix`;
CREATE TABLE `heroic_mobs_groups_fix`  (
  `map` int(11) NOT NULL,
  `cell` int(11) NOT NULL,
  `objects` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `group` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT ''
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for houses
-- ----------------------------
DROP TABLE IF EXISTS `houses`;
CREATE TABLE `houses`  (
  `id` int(10) UNSIGNED NOT NULL,
  `owner_id` int(11) NOT NULL DEFAULT 0,
  `sale` int(11) NOT NULL DEFAULT 1000000,
  `guild_id` int(11) NOT NULL DEFAULT 0,
  `access` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `key` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '-',
  `guild_rights` int(10) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for interactive_doors
-- ----------------------------
DROP TABLE IF EXISTS `interactive_doors`;
CREATE TABLE `interactive_doors`  (
  `maps` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `doorsEnable` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `doorsDisable` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `cellsEnable` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `cellsDisable` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `requiredCells` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
  `button` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '-1',
  `time` int(11) NOT NULL DEFAULT 30
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for interactive_objects_data
-- ----------------------------
DROP TABLE IF EXISTS `interactive_objects_data`;
CREATE TABLE `interactive_objects_data`  (
  `id` int(11) NOT NULL,
  `respawn` int(11) NOT NULL DEFAULT 10000,
  `duration` int(11) NOT NULL DEFAULT 1500,
  `unknow` int(11) NOT NULL DEFAULT 4,
  `walkable` int(11) NOT NULL DEFAULT 1,
  `Name IO` mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  UNIQUE INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for item_template
-- ----------------------------
DROP TABLE IF EXISTS `item_template`;
CREATE TABLE `item_template`  (
  `id` int(11) NOT NULL DEFAULT -1,
  `type` int(11) NOT NULL DEFAULT -1,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `level` int(11) NOT NULL DEFAULT 1,
  `statsTemplate` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `pod` int(11) NOT NULL DEFAULT 0,
  `panoplie` int(11) NOT NULL DEFAULT -1,
  `prix` int(11) NOT NULL DEFAULT 0 COMMENT 'prix de vente PAR un Npc',
  `conditions` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `armesInfos` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `sold` int(11) NOT NULL DEFAULT 0,
  `avgPrice` int(11) NOT NULL DEFAULT 0,
  `points` int(11) NOT NULL DEFAULT 0,
  `exchangesObject` int(11) NOT NULL DEFAULT 0,
  `newPrice` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for itemsets
-- ----------------------------
DROP TABLE IF EXISTS `itemsets`;
CREATE TABLE `itemsets`  (
  `ID` int(11) NOT NULL DEFAULT 0,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `items` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `bonus` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'bonus2items1,bonus2items2;bonus3items1,bonus3items2',
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for jobs_data
-- ----------------------------
DROP TABLE IF EXISTS `jobs_data`;
CREATE TABLE `jobs_data`  (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tools` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'outils utilisables',
  `crafts` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'templateID craftable',
  `skills` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `AP` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  UNIQUE INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for maps
-- ----------------------------
DROP TABLE IF EXISTS `maps`;
CREATE TABLE `maps`  (
  `id` int(11) NOT NULL,
  `date` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `width` int(11) NOT NULL DEFAULT -1,
  `heigth` int(11) NOT NULL DEFAULT -1,
  `places` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '|',
  `key` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mapData` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `monsters` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `capabilities` int(11) NOT NULL,
  `mappos` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0,0,0',
  `numgroup` int(11) NOT NULL DEFAULT 3,
  `minSize` int(11) NOT NULL DEFAULT 1,
  `fixSize` int(11) NOT NULL DEFAULT -1,
  `maxSize` int(11) NOT NULL DEFAULT 8,
  `forbidden` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0;0;0;0;0;0;0' COMMENT 'noMarchand;noCollector;noPrism;noTP;noDefie;noAgro;noCanal',
  `sniffed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for mobgroups_fix
-- ----------------------------
DROP TABLE IF EXISTS `mobgroups_fix`;
CREATE TABLE `mobgroups_fix`  (
  `mapid` int(11) NOT NULL,
  `cellid` int(11) NOT NULL,
  `groupData` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Donjon` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Salle` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Timer` int(11) NOT NULL DEFAULT 30000,
  PRIMARY KEY (`mapid`, `cellid`) USING BTREE,
  INDEX `mapid`(`mapid`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for monsters
-- ----------------------------
DROP TABLE IF EXISTS `monsters`;
CREATE TABLE `monsters`  (
  `id` int(11) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gfxID` int(11) NOT NULL,
  `align` int(11) NOT NULL,
  `grades` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `colors` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '-1,-1,-1',
  `stats` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'For,Sag,Int,Cha,Agi',
  `statsInfos` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0;0;0;1' COMMENT 'dmg;%dmg;soins;créainv',
  `spells` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pdvs` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1|1|1|1|1|1|1|1|1|1',
  `points` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1;1|1;1|1;1|1;1|1;1|1;1|1;1|1;1|1;1|1;1',
  `inits` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1|1|1|1|1|1|1|1|1|1',
  `minKamas` int(11) NOT NULL DEFAULT 0,
  `maxKamas` int(11) NOT NULL DEFAULT 0,
  `exps` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1|1|1|1|1|1|1|1|1|1',
  `AI_Type` int(11) NOT NULL DEFAULT 1 COMMENT '0: poutch 1: Agressif 2: Fuyarde 3: Soutient 4: Spécial',
  `capturable` int(11) NOT NULL DEFAULT 1,
  `type` int(11) NOT NULL DEFAULT 1 COMMENT '1 : Monster, 2 : Mascotte, 3 : Archi monster',
  `aggroDistance` tinyint(4) NULL DEFAULT 0,
  `isBoss` tinyint(4) NULL DEFAULT 0,
  `isArchmonster` tinyint(4) NULL DEFAULT 0,
  UNIQUE INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for mountpark_data
-- ----------------------------
DROP TABLE IF EXISTS `mountpark_data`;
CREATE TABLE `mountpark_data`  (
  `mapid` int(11) NOT NULL,
  `owner` int(11) NOT NULL,
  `guild` int(11) NOT NULL DEFAULT -1,
  `price` int(11) NOT NULL,
  `data` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'Etable',
  `enclos` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ObjetPlacer` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `durabilite` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`mapid`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for npc_questions
-- ----------------------------
DROP TABLE IF EXISTS `npc_questions`;
CREATE TABLE `npc_questions`  (
  `ID` int(11) NOT NULL,
  `responses` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `params` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `cond` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ifFalse` varchar(110) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for npc_reponses_actions
-- ----------------------------
DROP TABLE IF EXISTS `npc_reponses_actions`;
CREATE TABLE `npc_reponses_actions`  (
  `ID` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `args` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nom` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`ID`, `type`) USING BTREE,
  INDEX `ID`(`ID`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for npc_template
-- ----------------------------
DROP TABLE IF EXISTS `npc_template`;
CREATE TABLE `npc_template`  (
  `id` int(11) NOT NULL,
  `bonusValue` int(11) NOT NULL,
  `gfxID` int(11) NOT NULL,
  `scaleX` int(11) NOT NULL,
  `scaleY` int(11) NOT NULL,
  `sex` int(11) NOT NULL,
  `color1` int(11) NOT NULL,
  `color2` int(11) NOT NULL,
  `color3` int(11) NOT NULL,
  `accessories` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0,0,0,0',
  `extraClip` int(11) NOT NULL DEFAULT -1,
  `customArtWork` int(11) NOT NULL DEFAULT 0,
  `initQuestion` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ventes` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `quests` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `exchanges` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `informations` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for npcs
-- ----------------------------
DROP TABLE IF EXISTS `npcs`;
CREATE TABLE `npcs`  (
  `mapid` int(11) NOT NULL,
  `npcid` int(11) NOT NULL,
  `cellid` int(11) NOT NULL,
  `orientation` int(11) NOT NULL,
  `isMovable` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`mapid`, `npcid`, `cellid`) USING BTREE,
  INDEX `mapid`(`mapid`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Fixed;


-- ----------------------------
-- Table structure for objectsactions
-- ----------------------------
DROP TABLE IF EXISTS `objectsactions`;
CREATE TABLE `objectsactions`  (
  `template` int(11) NOT NULL DEFAULT 0,
  `type` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `args` varchar(400) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`template`) USING BTREE,
  INDEX `template`(`template`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for percepteurs
-- ----------------------------
DROP TABLE IF EXISTS `percepteurs`;
CREATE TABLE `percepteurs`  (
  `guid` int(11) NOT NULL AUTO_INCREMENT,
  `mapid` int(11) NOT NULL,
  `cellid` int(11) NOT NULL,
  `orientation` int(11) NOT NULL,
  `guild_id` int(11) NOT NULL,
  `poseur_id` int(11) NOT NULL,
  `date` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `N1` int(11) NOT NULL,
  `N2` int(11) NOT NULL,
  `objets` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `kamas` int(11) NOT NULL,
  `xp` int(11) NOT NULL,
  PRIMARY KEY (`guid`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for pets
-- ----------------------------
DROP TABLE IF EXISTS `pets`;
CREATE TABLE `pets`  (
  `Familier` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'Undefined',
  `TemplateID` int(11) NOT NULL,
  `Type` int(11) NOT NULL,
  `Gap` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `StatsUp` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Max` int(11) NOT NULL,
  `Gain` int(11) NOT NULL,
  `DeadTemplate` int(11) NOT NULL DEFAULT 0,
  `Epo` int(11) NOT NULL DEFAULT 0,
  `StatsMax` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `jet` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  UNIQUE INDEX `TemplateID`(`TemplateID`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for prismes
-- ----------------------------
DROP TABLE IF EXISTS `prismes`;
CREATE TABLE `prismes`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alignement` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `carte` int(11) NOT NULL,
  `celda` int(11) NOT NULL,
  `area` int(11) NOT NULL DEFAULT -1,
  `honor` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Fixed;


-- ----------------------------
-- Table structure for quest
-- ----------------------------
DROP TABLE IF EXISTS `quest`;
CREATE TABLE `quest`  (
  `id` int(11) NOT NULL,
  `nom` varchar(220) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `objectives` varchar(3201) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `steps` varchar(220) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `npc` int(11) NOT NULL,
  `action` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `args` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `deleteFinish` int(11) NOT NULL DEFAULT 0,
  `condition` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for quest_objective
-- ----------------------------
DROP TABLE IF EXISTS `quest_objective`;
CREATE TABLE `quest_objective`  (
  `id` int(11) NOT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `quest_data` int(11) NOT NULL,
  `quest_step` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `npc` int(11) NOT NULL,
  `item` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `monster` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `conditions` varchar(220) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '0',
  `validationType` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for quest_progress
-- ----------------------------
DROP TABLE IF EXISTS `quest_progress`;
CREATE TABLE `quest_progress`  (
  `account_id` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `quest_id` int(11) NOT NULL,
  `current_step` int(11) NOT NULL,
  `completed_objectives` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `finished` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`account_id`, `player_id`, `quest_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for quest_step
-- ----------------------------
DROP TABLE IF EXISTS `quest_step`;
CREATE TABLE `quest_step`  (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `xp` int(11) NOT NULL,
  `kamas` int(11) NOT NULL,
  `item` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'actionID|args;actionID|args',
  `asitem` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for runes
-- ----------------------------
DROP TABLE IF EXISTS `runes`;
CREATE TABLE `runes`  (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `bonus` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `weight` float(11, 2) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for schemafights
-- ----------------------------
DROP TABLE IF EXISTS `schemafights`;
CREATE TABLE `schemafights`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `places` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '|',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 97 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for scripted_cells
-- ----------------------------
DROP TABLE IF EXISTS `scripted_cells`;
CREATE TABLE `scripted_cells`  (
  `MapID` int(11) NOT NULL,
  `CellID` int(11) NOT NULL,
  `ActionID` int(11) NOT NULL,
  `EventID` int(11) NOT NULL,
  `ActionsArgs` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Conditions` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`MapID`, `CellID`) USING BTREE,
  INDEX `MapID`(`MapID`) USING BTREE,
  INDEX `CellID`(`CellID`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for sorts
-- ----------------------------
DROP TABLE IF EXISTS `sorts`;
CREATE TABLE `sorts`  (
  `id` int(11) NOT NULL,
  `nom` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sprite` int(11) NOT NULL DEFAULT -1,
  `spriteInfos` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0,0,0',
  `lvl1` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `lvl2` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `lvl3` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `lvl4` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `lvl5` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `lvl6` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `effectTarget` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` int(11) NOT NULL DEFAULT 0,
  `duration` int(11) NOT NULL DEFAULT 800,
  `invalid_state` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `needed_state` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  UNIQUE INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for subarea_data
-- ----------------------------
DROP TABLE IF EXISTS `subarea_data`;
CREATE TABLE `subarea_data`  (
  `id` int(11) NOT NULL,
  `alignement` int(11) NOT NULL DEFAULT 0,
  `conquistable` int(11) NOT NULL DEFAULT 0,
  `prisme` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id`(`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Fixed;


-- ----------------------------
-- Table structure for tutoriel
-- ----------------------------
DROP TABLE IF EXISTS `tutoriel`;
CREATE TABLE `tutoriel`  (
  `id` int(11) NOT NULL DEFAULT 0,
  `start` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reward1` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reward2` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reward3` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `reward4` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `end` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for zaapi
-- ----------------------------
DROP TABLE IF EXISTS `zaapi`;
CREATE TABLE `zaapi`  (
  `mapid` int(11) NOT NULL,
  `align` int(11) NOT NULL,
  PRIMARY KEY (`mapid`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Fixed;


SET FOREIGN_KEY_CHECKS = 1;
