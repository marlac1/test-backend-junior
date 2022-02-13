-- depends: 0001_init

INSERT INTO players (id, nickname, phone_number, gender)
VALUES
("9b5662a2-34ae-4131-935a-1ed9b850df38", "Switchelven", "+3367859663219", "male"),
("4ff8e05b-1bc7-4099-83e1-3894039535a2", "Robzer", "+33594669854", "male"),
("704363db-bb1b-4e84-a68a-b07ce3a53690", "Zyzo", "+33354634211", "male"),
("d2b85d9b-1986-4ca4-a3e8-f0dca5381513", "Dododo", "+33525977064", "male"),
("f2fc5b45-2a4b-456b-b4dc-0560ba3de95f", "Coco", "+33585540525", "male"),
("c13549ff-0f13-43a4-ac20-ecc8e84239b6", "BOY Admin", "+33189146177", "female"),
("16f412a1-1163-4eeb-8912-3b8043df1d0d", "WillViosa", "+3338347248", "female"),
("85045723-2763-4095-9183-9aa1c882c708", "jrmurloc", "+33791253048", "male");


INSERT INTO conversations (id, created_at)
VALUES
("9b5662a2-34ae-4131-935a-1ed9b850df38", 'now'),
("4ff8e05b-1bc7-4099-83e1-3894039535a2", 'now'),
("704363db-bb1b-4e84-a68a-b07ce3a53690", 'now'),
("d2b85d9b-1986-4ca4-a3e8-f0dca5381513", 'now'),
("f2fc5b45-2a4b-456b-b4dc-0560ba3de95f", 'now'),
("c13549ff-0f13-43a4-ac20-ecc8e84239b6", 'now'),
("16f412a1-1163-4eeb-8912-3b8043df1d0d", 'now'),
("85045723-2763-4095-9183-9aa1c882c708", 'now');

INSERT INTO conversation_players (conversation_id, player_id)
VALUES
("9b5662a2-34ae-4131-935a-1ed9b850df38", "9b5662a2-34ae-4131-935a-1ed9b850df38"),
("9b5662a2-34ae-4131-935a-1ed9b850df38", "4ff8e05b-1bc7-4099-83e1-3894039535a2"),
("4ff8e05b-1bc7-4099-83e1-3894039535a2", "9b5662a2-34ae-4131-935a-1ed9b850df38"),
("4ff8e05b-1bc7-4099-83e1-3894039535a2", "704363db-bb1b-4e84-a68a-b07ce3a53690"),
("704363db-bb1b-4e84-a68a-b07ce3a53690", "9b5662a2-34ae-4131-935a-1ed9b850df38"),
("704363db-bb1b-4e84-a68a-b07ce3a53690", "f2fc5b45-2a4b-456b-b4dc-0560ba3de95f"),
("d2b85d9b-1986-4ca4-a3e8-f0dca5381513", "9b5662a2-34ae-4131-935a-1ed9b850df38"),
("d2b85d9b-1986-4ca4-a3e8-f0dca5381513", "16f412a1-1163-4eeb-8912-3b8043df1d0d"),
("f2fc5b45-2a4b-456b-b4dc-0560ba3de95f", "16f412a1-1163-4eeb-8912-3b8043df1d0d"),
("f2fc5b45-2a4b-456b-b4dc-0560ba3de95f", "f2fc5b45-2a4b-456b-b4dc-0560ba3de95f"),
("c13549ff-0f13-43a4-ac20-ecc8e84239b6", "d2b85d9b-1986-4ca4-a3e8-f0dca5381513"),
("c13549ff-0f13-43a4-ac20-ecc8e84239b6", "704363db-bb1b-4e84-a68a-b07ce3a53690"),
("85045723-2763-4095-9183-9aa1c882c708", "4ff8e05b-1bc7-4099-83e1-3894039535a2"),
("85045723-2763-4095-9183-9aa1c882c708", "85045723-2763-4095-9183-9aa1c882c708");

INSERT INTO conversation_messages (id, conversation_id, send_by, content, attachments, metadata, send_at)
VALUES
("rMGJTu8x5xvi", "9b5662a2-34ae-4131-935a-1ed9b850df38", "9b5662a2-34ae-4131-935a-1ed9b850df38", "Test", NULL, NULL, "2016-10-21 10:00:59"),
("mgnckYDB0xlY", "9b5662a2-34ae-4131-935a-1ed9b850df38", "9b5662a2-34ae-4131-935a-1ed9b850df38", "Working ?", NULL, NULL, "2016-10-21 10:01:00"),
("42N3s7R6kw4s", "9b5662a2-34ae-4131-935a-1ed9b850df38", "9b5662a2-34ae-4131-935a-1ed9b850df38", "Should notify", NULL, NULL, "2016-10-21 10:15:00"),
("53KQ4b0qRZaO", "9b5662a2-34ae-4131-935a-1ed9b850df38", "9b5662a2-34ae-4131-935a-1ed9b850df38", "Ok storage", NULL, NULL, "2016-10-21 11:00:59"),
("hSTxxnouPViJ", "9b5662a2-34ae-4131-935a-1ed9b850df38", "9b5662a2-34ae-4131-935a-1ed9b850df38", "Hello @Robzer", NULL, NULL, "2016-10-21 11:02:35"),
("9dKn51xEQoWI", "9b5662a2-34ae-4131-935a-1ed9b850df38", "9b5662a2-34ae-4131-935a-1ed9b850df38", "Ping @Robzer", NULL, NULL, "2016-10-21 12:00:00");