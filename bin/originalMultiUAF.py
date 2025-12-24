import os, struct, json, math, sys
sys.path.append("bin")
import hashesDictionary

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

def unpackInt32():
    value = struct.unpack(">i", Tpl.read(4))[0]
    return value

def unpackUInt32():
    value = struct.unpack(">I", Tpl.read(4))[0]
    return value

def unpackStr8():
    length = struct.unpack(">I", Tpl.read(4))[0]
    text = Tpl.read(length).decode("utf8")
    return text

def unpackFloat32():
    value = struct.unpack(">f", Tpl.read(4))[0]
    return value

def unpackLongPath():
    lengthFile = struct.unpack(">I", Tpl.read(4))[0]
    file = Tpl.read(lengthFile).decode("utf8")
    lengthPath = struct.unpack(">I", Tpl.read(4))[0]
    path = Tpl.read(lengthPath).decode("utf8")
    stringID = struct.unpack(">I", Tpl.read(4))[0]
    pathFlag = struct.unpack(">I", Tpl.read(4))[0]
    return path + file

def beautifyFloat(val):
    if isinstance(val, list):
        return [beautifyFloat(v) for v in val]
    if val % 1 == 0:
        return int(val)
    return round(val, 6)

for root, dirs, folders in os.walk("input"):
    for inputFile in folders:

        if inputFile.endswith(".tpl.ckd"):
            inputFilePath = os.path.join(root, inputFile)
            print(f"\n-- Deserializing: {inputFile}")

            with open(inputFilePath, "rb") as Tpl:
                flag = unpackUInt32()
                structSize = unpackUInt32()

                dummyActor_Template = {
                    "__class": "Actor_Template",
                    "WIP": 0,
                    "LOWUPDATE": 0,
                    "UPDATE_LAYER": 0,
                    "PROCEDURAL": 0,
                    "STARTPAUSED": 0,
                    "FORCEISENVIRONMENT": 0,
                    "TAGS": [],
                    "COMPONENTS": []
                }

                Actor_Template = unpackUInt32()
                structSize = unpackUInt32()
                WIP = unpackUInt32(); dummyActor_Template["WIP"] = WIP
                LOWUPDATE = unpackUInt32(); dummyActor_Template["LOWUPDATE"] = LOWUPDATE
                UPDATE_LAYER = unpackUInt32(); dummyActor_Template["UPDATE_LAYER"] = UPDATE_LAYER
                PROCEDURAL = unpackUInt32(); dummyActor_Template["PROCEDURAL"] = PROCEDURAL
                STARTPAUSED = unpackUInt32(); dummyActor_Template["STARTPAUSED"] = STARTPAUSED
                FORCEISENVIRONMENT = unpackUInt32(); dummyActor_Template["FORCEISENVIRONMENT"] = FORCEISENVIRONMENT
                TAGS = Tpl.read(4)

                lenCOMPONENTS = unpackUInt32()
                for i in range(lenCOMPONENTS):
                    COMPONENT = Tpl.read(4)
                    if COMPONENT in hashesDictionary.Hashes:
                        strCOMPONENT = hashesDictionary.Hashes[COMPONENT]
                        print(f"------ Detected COMPONENTS: {strCOMPONENT}")

                        if strCOMPONENT == "JD_SongDescTemplate":
                            dummyCOMPONENT = {
                                "__class": "JD_SongDescTemplate",
                                "MapName": "NoMapName",
                                "JDVersion": -1,
                                "OriginalJDVersion": -1,
                                "RelatedAlbums": [],
                                "GameModes": [],
                                "Artist": "Unknown Artist",
                                "DancerName": "Unknown Dancer",
                                "Title": "Unknown Title",
                                "NumCoach": 1,
                                "MainCoach": -1,
                                "Difficulty": 2,
                                "BackgroundType": 0,
                                "LyricsType": 0,
                                "Energy": 1,
                                "AudioPreviewFadeTime": 0.5,
                                "AudioPreviews": [],
                                "DefaultColors": {},
                                "Paths": {
                                    "Avatars": None,
                                    "AsyncPlayers": None
                                }
                            }

                            structSize = unpackUInt32()
                            MapName = unpackStr8(); dummyCOMPONENT["MapName"] = MapName
                            JDVersion = unpackInt32(); dummyCOMPONENT["JDVersion"] = JDVersion
                            OriginalJDVersion = unpackInt32(); dummyCOMPONENT["OriginalJDVersion"] = OriginalJDVersion

                            lenRelatedAlbums = unpackUInt32()
                            RelatedAlbums = []
                            for i in range(lenRelatedAlbums):
                                RelatedAlbum = unpackStr8()
                                RelatedAlbums.append(RelatedAlbum)
                            dummyCOMPONENT["RelatedAlbums"] = RelatedAlbums

                            lenGameModes = unpackUInt32()
                            listGameModes = []
                            for i in range(lenGameModes):
                                dummyGameModeDesc = {
                                    "__class": "GameModeDesc",
                                    "Mode": 6,
                                    "Flags": 0,
                                    "NumCoach": 7,
                                    "LocaleID": 4294967295,
                                    "Status": 3,
                                    "Mojo_value": 0,
                                    "Colors": 0,
                                    "Config_template": "",
                                    "CountInProgression": 1
                                }

                                structSize = unpackUInt32()
                                Mode = unpackUInt32(); dummyGameModeDesc["Mode"] = Mode
                                Flags = unpackUInt32(); dummyGameModeDesc["Flags"] = Flags
                                NumCoach = unpackUInt32(); dummyGameModeDesc["NumCoach"] = NumCoach
                                LocaleID = unpackUInt32(); dummyGameModeDesc["LocaleID"] = LocaleID
                                Status = unpackInt32(); dummyGameModeDesc["Status"] = Status
                                Mojo_value = unpackUInt32(); dummyGameModeDesc["Mojo_value"] = Mojo_value
                                Colors = unpackInt32(); dummyGameModeDesc["Colors"] = Colors
                                Config_template = unpackLongPath(); dummyGameModeDesc["Config_template"] = Config_template
                                CountInProgression = unpackInt32(); dummyGameModeDesc["CountInProgression"] = CountInProgression
                                listGameModes.append(dummyGameModeDesc)
                            dummyCOMPONENT["GameModes"] = listGameModes

                            Artist = unpackStr8(); dummyCOMPONENT["Artist"] = Artist
                            DancerName = unpackStr8(); dummyCOMPONENT["DancerName"] = DancerName
                            Title = unpackStr8(); dummyCOMPONENT["Title"] = Title
                            NumCoach = unpackUInt32(); dummyCOMPONENT["NumCoach"] = NumCoach
                            MainCoach = unpackInt32(); dummyCOMPONENT["MainCoach"] = MainCoach
                            Difficulty = unpackUInt32(); dummyCOMPONENT["Difficulty"] = Difficulty
                            BackgroundType = unpackUInt32(); dummyCOMPONENT["BackgroundType"] = BackgroundType
                            LyricsType = unpackInt32(); dummyCOMPONENT["LyricsType"] = LyricsType
                            Energy = unpackUInt32(); dummyCOMPONENT["Energy"] = Energy
                            AudioPreviewFadeTime = unpackFloat32(); dummyCOMPONENT["AudioPreviewFadeTime"] = AudioPreviewFadeTime

                            lenAudioPreviews = unpackUInt32()
                            listAudioPreviews = []
                            for i in range(lenAudioPreviews):
                                dummyAudioPreview = {
                                "__class": "AudioPreview",
                                "Name": "",
                                "Startbeat": 0,
                                "Endbeat": 0
                                }

                                structSize = unpackUInt32()
                                enumNameKey = {
                                    1866479568: "coverflow",
                                    2971648438: "prelobby"
                                }
                                nameKey = unpackUInt32(); Name = enumNameKey.get(nameKey, None); dummyAudioPreview["Name"] = Name
                                Startbeat = unpackInt32(); dummyAudioPreview["Startbeat"] = Startbeat
                                Endbeat = unpackInt32(); dummyAudioPreview["Endbeat"] = Endbeat
                                listAudioPreviews.append(dummyAudioPreview)
                            dummyCOMPONENT["AudioPreviews"] = listAudioPreviews

                            lenDefaultColors = unpackUInt32()
                            DefaultColors = {}
                            for i in range(lenDefaultColors):
                                enumColorsKey = {
                                    614992087: "songColor_2A",
                                    835957575: "lyrics",
                                    2631470027: "theme",
                                    2727528644: "songColor_1A",
                                    3188431139: "songColor_2B",
                                    4118961255: "songColor_1B"
                                }
                                dummyDefaultColors = {}
                                keyDefaultColor = unpackUInt32(); key = enumColorsKey.get(keyDefaultColor, None)
                                color = []
                                colorB = unpackFloat32()
                                colorG = unpackFloat32()
                                colorR = unpackFloat32()
                                colorA = unpackFloat32()
                                color.append(beautifyFloat(colorA))
                                color.append(beautifyFloat(colorR))
                                color.append(beautifyFloat(colorG))
                                color.append(beautifyFloat(colorB))
                                DefaultColors[key] = color
                                dummyCOMPONENT["DefaultColors"] = DefaultColors

                            lenAvatars = unpackUInt32()
                            listAvatars = []
                            for i in range(lenAvatars):
                                filePath = unpackLongPath()
                                listAvatars.append(filePath)
                            dummyCOMPONENT["Paths"]["Avatars"] = listAvatars if listAvatars else None

                            lenAsyncPlayers = unpackUInt32()
                            listAsyncPlayers = []
                            for i in range(lenAsyncPlayers):
                                filePath = unpackLongPath()
                                listAsyncPlayers.append(filePath)
                            dummyCOMPONENT["Paths"]["AsyncPlayers"] = listAsyncPlayers if listAsyncPlayers else None

                            dummyActor_Template["COMPONENTS"].append(dummyCOMPONENT)

                        else:
                            print(f"------ THERE'S AN ERROR INSIDE A COMPONENTS")
                            continue

                    else:
                        print(f"---- ERROR")
                        continue

            def cleaning(data, keys2Check):
                if isinstance(data, dict):
                    for key in list(data.keys()):
                        if key in keys2Check and not data[key]:
                            del data[key]
                        else:
                            cleaning(data[key], keys2Check)
                elif isinstance(data, list):
                    for item in data:
                        cleaning(item, keys2Check)
            keys2Remove = ["RelatedAlbums", "AudioPreviews", "COMPONENTS", "GameModes", "TAGS"]
            cleaning(dummyActor_Template, keys2Remove)

            inputFileRelativePath = os.path.relpath(inputFilePath, "input")
            outputPath = os.path.join("output", inputFileRelativePath)
            os.makedirs(os.path.dirname(outputPath), exist_ok=True)
            with open(outputPath, "w", encoding="utf-8") as s:
                json.dump(dummyActor_Template, s, ensure_ascii=False, separators=(",", ":"))
                print(f"-- Deserialized: {inputFile}")
            with open(outputPath, "ab") as f:
                f.write(b'\x00')