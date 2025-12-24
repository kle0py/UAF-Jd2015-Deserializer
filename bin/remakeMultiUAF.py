import os, struct, json, math, sys
sys.path.append("bin")
import hashesDictionary

os.makedirs("input", exist_ok=True)
remakeFormat = "output/remakeFormat"
os.makedirs(remakeFormat, exist_ok=True)

def unpackInt32():
    value = struct.unpack(">i", byte.read(4))[0]
    return value

def unpackUInt32():
    value = struct.unpack(">I", byte.read(4))[0]
    return value

def unpackStr8():
    length = struct.unpack(">I", byte.read(4))[0]
    text = byte.read(length).decode("utf8")
    return text

def unpackFloat32():
    value = struct.unpack(">f", byte.read(4))[0]
    return value

def unpackShortPath():
    lengthFile = struct.unpack(">I", byte.read(4))[0]
    file = byte.read(lengthFile).decode("utf8")
    lengthPath = struct.unpack(">I", byte.read(4))[0]
    path = byte.read(lengthPath).decode("utf8")
    return path + file

def unpackLongPath():
    lengthFile = struct.unpack(">I", byte.read(4))[0]
    file = byte.read(lengthFile).decode("utf8")
    lengthPath = struct.unpack(">I", byte.read(4))[0]
    path = byte.read(lengthPath).decode("utf8")
    stringID = struct.unpack(">I", byte.read(4))[0]
    pathFlag = struct.unpack(">I", byte.read(4))[0]
    return path + file

def beautifyFloat(val):
    if isinstance(val, list):
        return [beautifyFloat(v) for v in val]
    if isinstance(val, (int, float)):
        if val % 1 == 0:
            return int(val)
        return round(val, 6)
    return val

def cleaningLists(data):
    if isinstance(data, dict):
        for key in list(data.keys()):
            value = data[key]
            cleaningLists(value)
            if isinstance(value, list) and value == []:
                del data[key]
    elif isinstance(data, list):
        for item in data:
            cleaningLists(item)

mapsPath = input("\n'World/Jd2015' to 'World/MAPS' [y/n]? ")

for root, dirs, folders in os.walk("input"):
    for inputFile in folders:

        if inputFile.endswith(".msh.ckd"):
            inputFilePath = os.path.join(root, inputFile)
            print(f"\n-- Deserializing: {inputFile}")

            with open(inputFilePath, "rb") as byte:

                def MaterialLayer():
                    MaterialLayer = unpackUInt32()
                    Enabled = unpackUInt32()
                    TexAdressingModeU = unpackUInt32()
                    TexAdressingModeV = unpackUInt32()
                    Filtering = unpackUInt32()
                    DiffuseColorB = unpackFloat32()
                    DiffuseColorG = unpackFloat32()
                    DiffuseColorR = unpackFloat32()
                    DiffuseColorA = unpackFloat32()
                    TextureUsage = unpackUInt32()
                    lenUVModifiers = unpackUInt32()
                    UVModifiers = []

                    for x in range(lenUVModifiers):
                        UVModifier = unpackUInt32()
                        TranslationU = unpackFloat32()
                        TranslationV = unpackFloat32()
                        AnimTranslationU = unpackUInt32()
                        AnimTranslationV = unpackUInt32()
                        Rotation = unpackFloat32()
                        RotationOffsetU = unpackFloat32()
                        RotationOffsetV = unpackFloat32()
                        AnimRotation = unpackUInt32()
                        ScaleU = unpackFloat32()
                        ScaleV = unpackFloat32()
                        ScaleOffsetU = unpackFloat32()
                        ScaleOffsetV = unpackFloat32()

                        dummyUVModifier = {
                            "__class": "UVModifier",
                            "TranslationU": beautifyFloat(TranslationU),
                            "TranslationV": beautifyFloat(TranslationV),
                            "AnimTranslationU": AnimTranslationU,
                            "AnimTranslationV": AnimTranslationV,
                            "Rotation": beautifyFloat(Rotation),
                            "RotationOffsetU": beautifyFloat(RotationOffsetU),
                            "RotationOffsetV": beautifyFloat(RotationOffsetV),
                            "AnimRotation": AnimRotation,
                            "ScaleU": beautifyFloat(ScaleU),
                            "ScaleV": beautifyFloat(ScaleV),
                            "ScaleOffsetU": beautifyFloat(ScaleOffsetU),
                            "ScaleOffsetV": beautifyFloat(ScaleOffsetV)
                        }

                        UVModifiers.append(dummyUVModifier)

                    return {
                        "__class": "MaterialLayer",
                        "Enabled": Enabled,
                        "AlphaThreshold": -1,
                        "TexAdressingModeU": TexAdressingModeU,
                        "TexAdressingModeV": TexAdressingModeV,
                        "Filtering": Filtering,
                        "DiffuseColor": [beautifyFloat(DiffuseColorA), beautifyFloat(DiffuseColorR), beautifyFloat(DiffuseColorG), beautifyFloat(DiffuseColorB)],
                        "TextureUsage": TextureUsage,
                        "UVModifiers": UVModifiers
                    }

                byte.read(4)
                structSize = unpackUInt32()
                GFXMaterialShader_Template = unpackUInt32()
                byte.read(4)
                flags = unpackUInt32()
                renderRegular = unpackUInt32()
                renderFrontLight = unpackUInt32()
                renderBackLight = unpackUInt32()
                useAlphaTest = unpackUInt32()
                alphaRef = unpackUInt32()
                separateAlpha = unpackUInt32()
                byte.read(4)
                textureBlend = unpackUInt32()
                materialtype = unpackUInt32()
                lightingType = unpackUInt32()
                GFX_MaterialParams = unpackUInt32()
                matParams0F = unpackUInt32()
                matParams1F = unpackUInt32()
                matParams2F = unpackUInt32()
                matParams3F = unpackUInt32()
                matParams0I = unpackUInt32()
                matParams0VX = unpackUInt32()
                matParams0VY = unpackUInt32()
                matParams0VZ = unpackUInt32()
                matParams0VW = unpackUInt32()
                blendmode = unpackUInt32()
                Layer1 = MaterialLayer()
                BlendLayer2 = unpackUInt32()
                Layer2 = MaterialLayer()
                BlendLayer3 = unpackUInt32()
                Layer3 = MaterialLayer()
                BlendLayer4 = unpackUInt32()
                Layer4 = MaterialLayer()

                dummyGFXMaterialShader_Template = {
                    "__class": "GFXMaterialShader_Template",
                    "flags": flags,
                    "renderRegular": renderRegular,
                    "renderFrontLight": renderFrontLight,
                    "renderBackLight": renderBackLight,
                    "useAlphaTest": useAlphaTest,
                    "alphaRef": alphaRef,
                    "separateAlpha": separateAlpha,
                    "textureBlend": textureBlend,
                    "materialtype": materialtype,
                    "lightingType": lightingType,
                    "matParams": {
                        "__class": "GFX_MaterialParams",
                        "matParams0F": matParams0F,
                        "matParams1F": matParams1F,
                        "matParams2F": matParams2F,
                        "matParams3F": matParams3F,
                        "matParams0I": matParams0I,
                        "matParams0VX": matParams0VX,
                        "matParams0VY": matParams0VY,
                        "matParams0VZ": matParams0VZ,
                        "matParams0VW": matParams0VW
                    },
                    "blendmode": blendmode,
                    "Layer1": Layer1,
                    "BlendLayer2": BlendLayer2,
                    "Layer2": Layer2,
                    "BlendLayer3": BlendLayer3,
                    "Layer3": Layer3,
                    "BlendLayer4": BlendLayer4,
                    "Layer4": Layer4
                }

            cleaningLists(dummyGFXMaterialShader_Template)
            inputFileRelativePath = os.path.relpath(inputFilePath, "input")
            outputPath = os.path.join(remakeFormat, inputFileRelativePath)
            os.makedirs(os.path.dirname(outputPath), exist_ok=True)
            with open(outputPath, "w", encoding="utf-8") as s:
                json.dump(dummyGFXMaterialShader_Template, s, ensure_ascii=False, separators=(",", ":"))
                print(f"\033[32m-- Deserialized:\033[0m {inputFile}")
            with open(outputPath, "ab") as f:
                f.write(b'\x00')

        if inputFile.endswith((".tape.ckd", ".dtape.ckd", "ktape.ckd", "stape.ckd", "btape.ckd")):
            inputFilePath = os.path.join(root, inputFile)
            print(f"\n-- Deserializing: {inputFile}")

            # List of all the curves
            strCurve = "Curve"; strCurveA = "CurveA"; strCurveR = "CurveR"; strCurveG = "CurveG"; strCurveB = "CurveB"; strCurveRed = "CurveRed"; strCurveGreen = "CurveGreen"
            strCurveBlue = "CurveBlue"; strCurveU = "CurveU"; strCurveV = "CurveV"; strCurveX = "CurveX"; strCurveY = "CurveY"; strCurveZ = "CurveZ"; strCurveSizeX = "CurveSizeX"
            strCurveSizeY = "CurveSizeY"; strCurveAngle = "CurveAngle"; strCurvePivotX = "CurvePivotX"; strCurvePivotY = "CurvePivotY"; strCurveScaleU = "CurveScaleU"
            strCurveScaleV = "CurveScaleV"; strCurveScrollU = "CurveScrollU"; strCurveScrollV = "CurveScrollV"

            def curve(byte, bezierType, curveType, hashesDictionary):
                if bezierType in hashesDictionary.Hashes:
                    strBezierType = hashesDictionary.Hashes[bezierType]
                    print(f"---------- Detected bezierType: {strBezierType} for {curveType}")

                    if strBezierType == "NULL":
                        dummyClip[curveType] = {
                            "__class": "BezierCurveFloat",
                            "Curve": {}
                        }

                    elif strBezierType == "BezierCurveFloatConstant":
                        lenCurve = unpackUInt32()
                        Value = unpackFloat32()
                        dummyClip[curveType] = {
                            "__class": "BezierCurveFloat",
                            "Curve": {
                                "__class": "BezierCurveFloatConstant",
                                "Value": beautifyFloat(Value)
                            }
                        }

                    elif strBezierType == "BezierCurveFloatLinear":
                        lenCurve = unpackUInt32()
                        ValueLeft = struct.unpack(">ff", byte.read(8))
                        NormalLeftOut = struct.unpack(">ff", byte.read(8))
                        ValueRight = struct.unpack(">ff", byte.read(8))
                        NormalRightIn = struct.unpack(">ff", byte.read(8))
                        dummyClip[curveType] = {
                            "__class": "BezierCurveFloat",
                            "Curve": {
                                "__class": "BezierCurveFloatLinear",
                                "ValueLeft": beautifyFloat(list(ValueLeft)),
                                "NormalLeftOut": beautifyFloat(list(NormalLeftOut)),
                                "ValueRight": beautifyFloat(list(ValueRight)),
                                "NormalRightIn": beautifyFloat(list(NormalRightIn))
                            }
                        }

                    elif strBezierType == "BezierCurveFloatMulti":
                        byte.read(4)
                        lenKeys = unpackUInt32()
                        dummyClip[curveType] = {
                            "__class": "BezierCurveFloat",
                            "Curve": {
                                "__class": "BezierCurveFloatMulti",
                                "Keys": []
                            }
                        }

                        for x in range(lenKeys):
                            byte.read(4)
                            Value = struct.unpack(">ff", byte.read(8))
                            NormalIn = struct.unpack(">ff", byte.read(8))
                            NormalOut = struct.unpack(">ff", byte.read(8))
                            dummyKeyFloat = {
                                "__class": "KeyFloat",
                                "Value": beautifyFloat(list(Value)),
                                "NormalIn": beautifyFloat(list(NormalIn)),
                                "NormalOut": beautifyFloat(list(NormalOut))
                            }
                            dummyClip[curveType]["Curve"]["Keys"].append(dummyKeyFloat)

                else:
                    print(f"\033[31m---------- ERROR\033[0m")

                return dummyClip if dummyClip else {curveType: {}}

            with open(inputFilePath, "rb") as byte:
                byte.read(4)
                structSize = unpackUInt32()
                Tape = unpackUInt32()
                byte.read(4)
                lenClips = unpackUInt32()

                dummyTape = {
                    "__class": "Tape",
                    "Clips": [],
                    "MetaInfos": [],
                    "ActorPaths": [],
                    "TapeClock": 2,
                    "TapeBarCount": 1,
                    "FreeResourcesAfterPlay": 0,
                    "MapName": "",
                }

                for x in range(lenClips):
                    Clip = byte.read(4)

                    if Clip in hashesDictionary.Hashes:
                        strClip = hashesDictionary.Hashes[Clip]
                        print(f"------ Detected Clip: {strClip}")

                        if strClip == "AlphaClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "Curve": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["Curve"] = curve(byte, bezierType, strCurve, hashesDictionary)["Curve"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "ColorClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "CurveRed": {},
                                "CurveGreen": {},
                                "CurveBlue": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveRed"] = curve(byte, bezierType, strCurveRed, hashesDictionary)["CurveRed"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveGreen"] = curve(byte, bezierType, strCurveGreen, hashesDictionary)["CurveGreen"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveBlue"] = curve(byte, bezierType, strCurveBlue, hashesDictionary)["CurveBlue"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "CommunityDancerClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            DancerCountryCode = unpackStr8()
                            DancerAvatarId = unpackUInt32()
                            DancerName = unpackStr8()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "DancerCountryCode": DancerCountryCode,
                                "DancerAvatarId": DancerAvatarId,
                                "DancerName": DancerName
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "FXClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            FxName = byte.read(4)
                            KillParticlesOnEnd = unpackUInt32()

                            if FxName in hashesDictionary.Hashes:
                                strFxName = hashesDictionary.Hashes[FxName]
                                print(f"---------- Detected FxName: {strFxName}")

                            else:
                                print(f"\033[33m---------- No FxName detected!\033[0m")
                                strFxName = None
                                continue

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "FxName": strFxName,
                                "KillParticlesOnEnd": KillParticlesOnEnd
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "GameplayEventClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            byte.read(4)
                            EventType = unpackUInt32()
                            CustomParam = unpackStr8()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "EventType": EventType,
                                "CustomParam": CustomParam
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "GoldEffectClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            EffectType = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "EffectType": EffectType
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "HideUserInterfaceClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            byte.read(4)
                            EventType = unpackUInt32()
                            CustomParam = unpackStr8()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "EventType": EventType,
                                "CustomParam": ""
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "KaraokeClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            Pitch = unpackFloat32()
                            Lyrics = unpackStr8()
                            IsEndOfLine = unpackUInt32()
                            ContentType = unpackUInt32()
                            StartTimeTolerance = unpackUInt32()
                            EndTimeTolerance = unpackUInt32()
                            SemitoneTolerance = unpackFloat32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "Pitch": beautifyFloat(Pitch),
                                "Lyrics": Lyrics,
                                "IsEndOfLine": IsEndOfLine,
                                "ContentType": ContentType,
                                "StartTimeTolerance": StartTimeTolerance,
                                "EndTimeTolerance": EndTimeTolerance,
                                "SemitoneTolerance": beautifyFloat(SemitoneTolerance)
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "MaterialGraphicDiffuseAlphaClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            LayerIdx = unpackUInt32()
                            UVModifierIdx = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "LayerIdx": LayerIdx,
                                "UVModifierIdx": UVModifierIdx,
                                "CurveA": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveA"] = curve(byte, bezierType, strCurveA, hashesDictionary)["CurveA"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "MaterialGraphicDiffuseColorClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            LayerIdx = unpackUInt32()
                            UVModifierIdx = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "LayerIdx": LayerIdx,
                                "UVModifierIdx": UVModifierIdx,
                                "CurveA": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveR"] = curve(byte, bezierType, strCurveR, hashesDictionary)["CurveR"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveG"] = curve(byte, bezierType, strCurveG, hashesDictionary)["CurveG"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveB"] = curve(byte, bezierType, strCurveB, hashesDictionary)["CurveB"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "MaterialGraphicEnableLayerClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            LayerIdx = unpackUInt32()
                            UVModifierIdx = unpackUInt32()
                            LayerEnabled = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "LayerIdx": LayerIdx,
                                "UVModifierIdx": UVModifierIdx,
                                "LayerEnabled": LayerEnabled
                            }

                            dummyClip["ActorIndices"] = ActorIndices

                        elif strClip == "MaterialGraphicUVRotationClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            LayerIdx = unpackUInt32()
                            UVModifierIdx = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "LayerIdx": LayerIdx,
                                "UVModifierIdx": UVModifierIdx,
                                "CurveAngle": {},
                                "CurvePivotX": {},
                                "CurvePivotY": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveAngle"] = curve(byte, bezierType, strCurveAngle, hashesDictionary)["CurveAngle"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurvePivotX"] = curve(byte, bezierType, strCurvePivotX, hashesDictionary)["CurvePivotX"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurvePivotY"] = curve(byte, bezierType, strCurvePivotY, hashesDictionary)["CurvePivotY"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "MaterialGraphicUVScaleClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            LayerIdx = unpackUInt32()
                            UVModifierIdx = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "LayerIdx": LayerIdx,
                                "UVModifierIdx": UVModifierIdx,
                                "CurveScaleU": {},
                                "CurveScaleV": {},
                                "CurvePivotX": {},
                                "CurvePivotY": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveScaleU"] = curve(byte, bezierType, strCurveScaleU, hashesDictionary)["CurveScaleU"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveScaleV"] = curve(byte, bezierType, strCurveScaleV, hashesDictionary)["CurveScaleV"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurvePivotX"] = curve(byte, bezierType, strCurvePivotX, hashesDictionary)["CurvePivotX"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurvePivotY"] = curve(byte, bezierType, strCurvePivotY, hashesDictionary)["CurvePivotY"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "MaterialGraphicUVScrollClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            LayerIdx = unpackUInt32()
                            UVModifierIdx = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "LayerIdx": LayerIdx,
                                "UVModifierIdx": UVModifierIdx,
                                "CurveScrollU": {},
                                "CurveScrollV": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveScrollU"] = curve(byte, bezierType, strCurveScrollU, hashesDictionary)["CurveScrollU"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveScrollV"] = curve(byte, bezierType, strCurveScrollV, hashesDictionary)["CurveScrollV"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "MaterialGraphicUVTranslationClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            LayerIdx = unpackUInt32()
                            UVModifierIdx = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "LayerIdx": LayerIdx,
                                "UVModifierIdx": UVModifierIdx,
                                "CurveU": {},
                                "CurveV": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveU"] = curve(byte, bezierType, strCurveU, hashesDictionary)["CurveU"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveV"] = curve(byte, bezierType, strCurveV, hashesDictionary)["CurveV"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "MotionClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            ClassifierPath = unpackLongPath()
                            GoldMove = unpackUInt32()
                            CoachId = unpackUInt32()
                            MoveType = unpackUInt32()
                            ColorB = unpackFloat32()
                            ColorG = unpackFloat32()
                            ColorR = unpackFloat32()
                            ColorA = unpackFloat32()
                            lenMotionPlatformSpecifics = unpackUInt32()
                            X360 = byte.read(4)
                            lenMotionPlatformSpecificX360 = unpackUInt32()
                            ScoreScaleX360 = unpackFloat32()
                            ScoreSmoothingX360 = unpackFloat32()
                            ScoringModeX360 = unpackUInt32()
                            ORBIS = byte.read(4)
                            lenMotionPlatformSpecificORBIS = unpackUInt32()
                            ScoreScaleORBIS = unpackFloat32()
                            ScoreSmoothingORBIS = unpackFloat32()
                            ScoringModeORBIS = unpackUInt32()
                            DURANGO = byte.read(4)
                            lenMotionPlatformSpecificDURANGO = unpackUInt32()
                            ScoreScaleDURANGO = unpackFloat32()
                            ScoreSmoothingDURANGO = unpackFloat32()
                            ScoringModeDURANGO = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ClassifierPath": ClassifierPath.replace("jd2015", "maps") if mapsPath == "y" else ClassifierPath,
                                "GoldMove": GoldMove,
                                "CoachId": CoachId,
                                "MoveType": MoveType,
                                "Color": [beautifyFloat(ColorA), beautifyFloat(ColorR), beautifyFloat(ColorG), beautifyFloat(ColorB)],
                                "MotionPlatformSpecifics": {
                                    "X360": {
                                        "__class": "MotionPlatformSpecific",
                                        "ScoreScale": beautifyFloat(ScoreScaleX360),
                                        "ScoreSmoothing": beautifyFloat(ScoreSmoothingX360),
                                        "ScoringMode": ScoringModeX360
                                    },
                                    "ORBIS": {
                                        "__class": "MotionPlatformSpecific",
                                        "ScoreScale": beautifyFloat(ScoreScaleORBIS),
                                        "ScoreSmoothing": beautifyFloat(ScoreSmoothingORBIS),
                                        "ScoringMode": ScoringModeORBIS
                                    },
                                    "DURANGO": {
                                        "__class": "MotionPlatformSpecific",
                                        "ScoreScale": beautifyFloat(ScoreScaleDURANGO),
                                        "ScoreSmoothing": beautifyFloat(ScoreSmoothingDURANGO),
                                        "ScoringMode": ScoringModeDURANGO
                                    }
                                }
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "PictogramClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            PictoPath = unpackLongPath()
                            CoachCount = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "PictoPath": PictoPath.replace("jd2015", "maps") if mapsPath == "y" else PictoPath,
                                "CoachCount": CoachCount,
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "ProportionClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "CurveX": {},
                                "CurveY": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveX"] = curve(byte, bezierType, strCurveX, hashesDictionary)["CurveX"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveY"] = curve(byte, bezierType, strCurveY, hashesDictionary)["CurveY"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "RotationClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "CurveX": {},
                                "CurveY": {},
                                "CurveZ": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveX"] = curve(byte, bezierType, strCurveX, hashesDictionary)["CurveX"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveY"] = curve(byte, bezierType, strCurveY, hashesDictionary)["CurveY"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveZ"] = curve(byte, bezierType, strCurveZ, hashesDictionary)["CurveZ"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "SizeClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "CurveX": {},
                                "CurveY": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveX"] = curve(byte, bezierType, strCurveX, hashesDictionary)["CurveX"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveY"] = curve(byte, bezierType, strCurveY, hashesDictionary)["CurveY"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "SlotClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            Bpm = unpackFloat32()
                            Signature = unpackStr8()
                            Guid = unpackStr8()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "Bpm": beautifyFloat(Bpm),
                                "Signature": Signature,
                                "Guid": Guid
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "SoundSetClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            SoundSetPath = unpackLongPath()
                            SoundChannel = unpackUInt32()
                            StopsOnEnd = unpackUInt32()
                            AccountedForDuration = unpackInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "SoundSetPath": SoundSetPath.replace("jd2015", "maps") if mapsPath == "y" else SoundSetPath,
                                "SoundChannel": SoundChannel,
                                "StopsOnEnd": StopsOnEnd,
                                "AccountedForDuration": AccountedForDuration
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "SpawnActorClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            ActorPath = unpackShortPath()
                            byte.read(4)
                            ActorName = unpackStr8()
                            SpawnPosition = unpackFloat32(), unpackFloat32(), unpackFloat32()
                            byte.read(4)
                            ParentActor = unpackLongPath()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "ActorPath": ActorPath,
                                "ActorName": ActorName,
                                "SpawnPosition": list(SpawnPosition),
                                "ParentActor": ParentActor
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "TapeLauncherClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            Action = unpackUInt32()
                            TapeLabel = byte.read(4)

                            if TapeLabel in hashesDictionary.Hashes:
                                strTapeLabel = hashesDictionary.Hashes[TapeLabel].upper()
                                print(f"---------- Detected TapeLabel: {strTapeLabel}")

                            else:
                                print(f"\033[33m---------- No TapeLabel detected!\033[0m")
                                strTapeLabel = None
                                continue

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "Action": Action,
                                "TapeLabel": strTapeLabel
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "TextClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            LocalizationKey = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "LocalizationKey": LocalizationKey
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "TapeReferenceClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            Path = unpackLongPath()
                            byte.read(4)
                            Loop = unpackUInt32()

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "Path": Path.replace("jd2015", "maps") if mapsPath == "y" else Path,
                                "Loop": Loop
                            }

                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "TranslationClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "CurveX": {},
                                "CurveY": {},
                                "CurveZ": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveX"] = curve(byte, bezierType, strCurveX, hashesDictionary)["CurveX"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveY"] = curve(byte, bezierType, strCurveY, hashesDictionary)["CurveY"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveZ"] = curve(byte, bezierType, strCurveZ, hashesDictionary)["CurveZ"]
                            dummyTape["Clips"].append(dummyClip)

                        elif strClip == "UICollBoxClip":
                            structSize = unpackUInt32()
                            Id = unpackUInt32()
                            TrackId = unpackUInt32()
                            IsActive = unpackUInt32()
                            StartTime = unpackInt32()
                            Duration = unpackInt32()
                            lenActorName = unpackUInt32()

                            ActorIndices = []
                            for x in range(lenActorName):
                                byte.read(4)
                                lenParts = unpackUInt32()
                                lenParts += 1

                                ActorNames = []
                                for x in range(lenParts):
                                    if x < lenParts - 1:
                                        byte.read(4)
                                    ActorName = unpackStr8()
                                    isDots = unpackUInt32()
                                    ActorNameSeparator = "..|" if isDots == 1 else "|"
                                    ActorNames.append(ActorName + (ActorNameSeparator if x < lenParts - 1 else ""))

                                fullActorNames = "".join(ActorNames)
                                if ActorNames not in dummyTape["ActorPaths"]:
                                    dummyTape["ActorPaths"].append(fullActorNames)
                                ActorIndex = dummyTape["ActorPaths"].index(fullActorNames)
                                ActorIndices.append(ActorIndex)

                            dummyClip = {
                                "__class": strClip,
                                "Id": Id,
                                "TrackId": TrackId,
                                "IsActive": IsActive,
                                "StartTime": StartTime,
                                "Duration": Duration,
                                "ActorIndices": [],
                                "CurveX": {},
                                "CurveY": {},
                                "CurveSizeX": {},
                                "CurveSizeY": {}
                            }

                            dummyClip["ActorIndices"] = ActorIndices
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveX"] = curve(byte, bezierType, strCurveX, hashesDictionary)["CurveX"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveY"] = curve(byte, bezierType, strCurveY, hashesDictionary)["CurveY"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveSizeX"] = curve(byte, bezierType, strCurveSizeX, hashesDictionary)["CurveSizeX"]
                            byte.read(4)
                            bezierType = byte.read(4)
                            dummyClip["CurveSizeY"] = curve(byte, bezierType, strCurveSizeY, hashesDictionary)["CurveSizeY"]
                            dummyTape["Clips"].append(dummyClip)

                        else:
                            print(f"\033[31m------ THERE'S AN ERROR WITH A CLIP\033[0m")
                            continue

                    else:
                        print(f"\033[31m---- ERROR\033[0m")
                        continue

                byte.read(4)
                lenMetaInfos = unpackUInt32()

                for x in range(lenMetaInfos):
                    MetaInfos = byte.read(4)

                    if MetaInfos in hashesDictionary.Hashes:
                        strMetaInfos = hashesDictionary.Hashes[MetaInfos]
                        print(f"------ Detected MetaInfos: {strMetaInfos}")

                        if strMetaInfos == "KaraokeMetaInfo":
                            structSize = unpackUInt32()
                            id = unpackUInt32()
                            WindowSize = unpackUInt32()
                            WindowHop = unpackUInt32()
                            RMSThreshold = unpackFloat32()
                            RMSTendencyToIncrease = unpackFloat32()
                            RMSTendencyToDecrease = unpackFloat32()
                            YinPitchTreshold = unpackFloat32()
                            PitchLowerBound = unpackFloat32()
                            PitchUpperBound = unpackFloat32()
                            HistorySpan = unpackUInt32()
                            SlidingMeanWindowSize = unpackUInt32()
                            SlidingMeanVariationThreshold = unpackFloat32()
                            NoPitchScoring = unpackUInt32()
                            GraphicsPitchMeanWindow = unpackUInt32()

                            dummyMetaInfo = {
                                "__class": "KaraokeMetaInfo",
                                "id": id,
                                "WindowSize": WindowSize,
                                "WindowHop": WindowHop,
                                "RMSThreshold": beautifyFloat(RMSThreshold),
                                "RMSTendencyToIncrease": beautifyFloat(RMSTendencyToIncrease),
                                "RMSTendencyToDecrease": beautifyFloat(RMSTendencyToDecrease),
                                "YinPitchTreshold": beautifyFloat(YinPitchTreshold),
                                "PitchLowerBound": beautifyFloat(PitchLowerBound),
                                "PitchUpperBound": beautifyFloat(PitchUpperBound),
                                "HistorySpan": HistorySpan,
                                "SlidingMeanWindowSize": SlidingMeanWindowSize,
                                "SlidingMeanVariationThreshold": beautifyFloat(SlidingMeanVariationThreshold),
                                "NoPitchScoring": NoPitchScoring,
                                "GraphicsPitchMeanWindow": GraphicsPitchMeanWindow
                            }

                            dummyTape["MetaInfos"].append(dummyMetaInfo)

                        else:
                            print(f"\033[31m------ THERE'S AN ERROR WITH A METAINFO\033[0m")
                            continue

                    else:
                        continue

                TapeClock = unpackUInt32()
                TapeBarCount = unpackUInt32()
                FreeResourcesAfterPlay = unpackUInt32()
                MapName = unpackStr8()
                dummyTape["TapeClock"] = TapeClock
                dummyTape["TapeBarCount"] = TapeBarCount
                dummyTape["FreeResourcesAfterPlay"] = FreeResourcesAfterPlay
                dummyTape["MapName"] = MapName

            cleaningLists(dummyTape)
            inputFileRelativePath = os.path.relpath(inputFilePath, "input")
            outputPath = os.path.join(remakeFormat, inputFileRelativePath)
            os.makedirs(os.path.dirname(outputPath), exist_ok=True)
            with open(outputPath, "w", encoding="utf-8") as s:
                json.dump(dummyTape, s, ensure_ascii=False, separators=(",", ":"))
                print(f"\033[32m-- Deserialized:\033[0m {inputFile}")
            with open(outputPath, "ab") as f:
                f.write(b'\x00')

        if inputFile.endswith(".tpl.ckd"):
            inputFilePath = os.path.join(root, inputFile)
            print(f"\n-- Deserializing: {inputFile}")

            with open(inputFilePath, "rb") as byte:
                byte.read(4)
                structSize = unpackUInt32()
                Actor_Template = unpackUInt32()
                structSize = unpackUInt32()
                WIP = unpackUInt32()
                LOWUPDATE = unpackUInt32()
                UPDATE_LAYER = unpackUInt32()
                PROCEDURAL = unpackUInt32()
                STARTPAUSED = unpackUInt32()
                FORCEISENVIRONMENT = unpackUInt32()
                TAGS = byte.read(4)
                lenCOMPONENTS = unpackUInt32()

                dummyActor_Template = {
                    "__class": "Actor_Template",
                    "WIP": WIP,
                    "LOWUPDATE": LOWUPDATE,
                    "UPDATE_LAYER": UPDATE_LAYER,
                    "PROCEDURAL": PROCEDURAL,
                    "STARTPAUSED": STARTPAUSED,
                    "FORCEISENVIRONMENT": FORCEISENVIRONMENT,
                    "TAGS": [],
                    "COMPONENTS": []
                }

                for x in range(lenCOMPONENTS):
                    COMPONENT = byte.read(4)

                    if COMPONENT in hashesDictionary.Hashes:
                        strCOMPONENT = hashesDictionary.Hashes[COMPONENT]
                        print(f"------ Detected COMPONENTS: {strCOMPONENT}")

                        if strCOMPONENT == "JD_AutodanceComponent_Template":
                            byte.read(4)
                            song = unpackStr8()
                            byte.read(8)
                            lenRecords = unpackUInt32()

                            dummyCOMPONENT = {
                                "__class": strCOMPONENT,
                                "song": song,
                                "autodanceData": {}
                            }

                            dummyAutodanceData = {
                                "__class": "JD_AutodanceData",
                                "recording_structure": {},
                                "video_structure": {},
                                "autodanceSoundPath": ""
                            }

                            dummyAutodanceRecordingStructure = {
                                "__class": "JD_AutodanceRecordingStructure",
                                "records": []
                            }

                            for x in range(lenRecords):
                                byte.read(4)
                                Start = unpackFloat32()
                                Duration = unpackFloat32()

                                dummyRecordData = {
                                    "__class": "Record",
                                    "Start": beautifyFloat(Start),
                                    "Duration": beautifyFloat(Duration)
                                }

                                dummyAutodanceRecordingStructure["records"].append(dummyRecordData)

                            byte.read(4)
                            GameMode = unpackUInt32()
                            SongStartPosition = unpackFloat32()
                            Duration = unpackFloat32()
                            ThumbnailTime = unpackFloat32()
                            FadeOutDuration = unpackFloat32()
                            AnimatedFramePath = unpackLongPath()
                            GroundPlanePath = unpackLongPath()
                            FirstLayerTripleBackgroundPath = unpackLongPath()
                            SecondLayerTripleBackgroundPath = unpackLongPath()
                            ThirdLayerTripleBackgroundPath = unpackLongPath()

                            dummyAutodanceVideoStructure = {
                                "__class": "JD_AutodanceVideoStructure",
                                "GameMode": GameMode,
                                "SongStartPosition": beautifyFloat(SongStartPosition),
                                "Duration": beautifyFloat(Duration),
                                "ThumbnailTime": beautifyFloat(ThumbnailTime),
                                "FadeOutDuration": beautifyFloat(FadeOutDuration),
                                "AnimatedFramePath": AnimatedFramePath,
                                "GroundPlanePath": GroundPlanePath,
                                "FirstLayerTripleBackgroundPath": FirstLayerTripleBackgroundPath,
                                "SecondLayerTripleBackgroundPath": SecondLayerTripleBackgroundPath,
                                "ThirdLayerTripleBackgroundPath": ThirdLayerTripleBackgroundPath,
                                "playback_events": [],
                                "background_effect": {},
                                "background_effect_events": [],
                                "player_effect": {},
                                "player_effect_events": [],
                                "prop_events": [],
                                "props": [],
                                "props_players_config": []
                            }

                            lenPlayback_events = unpackUInt32()

                            for x in range(lenPlayback_events):
                                byte.read(4)
                                ClipNumber = unpackInt32()
                                StartClip = unpackFloat32()
                                StartTime = unpackFloat32()
                                Duration = unpackFloat32()
                                Speed = unpackFloat32()

                                dummyPlaybackEventData = {
                                    "__class": "PlaybackEvent",
                                    "ClipNumber": ClipNumber,
                                    "StartClip": beautifyFloat(StartClip),
                                    "StartTime": beautifyFloat(StartTime),
                                    "Duration": beautifyFloat(Duration),
                                    "Speed": beautifyFloat(Speed)
                                }

                                dummyAutodanceVideoStructure["playback_events"].append(dummyPlaybackEventData)

                            def AutoDanceFxDesc():

                                def GFX_Vector4():
                                    structSize = unpackFloat32()
                                    x = unpackFloat32()
                                    y = unpackFloat32()
                                    z = unpackFloat32()
                                    w = unpackFloat32()

                                    return {
                                        "__class": "GFX_Vector4",
                                        "x": beautifyFloat(x),
                                        "y": beautifyFloat(y),
                                        "z": beautifyFloat(z),
                                        "w": beautifyFloat(w)
                                    }

                                AutoDanceFxDesc = byte.read(4)
                                Opacity = unpackFloat32()
                                ColorLow = GFX_Vector4()
                                ColorMid = GFX_Vector4()
                                ColorHigh = GFX_Vector4()
                                LowToMid = unpackFloat32()
                                LowToMidWidth = unpackFloat32()
                                MidToHigh = unpackFloat32()
                                MidToHighWidth = unpackFloat32()
                                SobColor = GFX_Vector4()
                                OutColor = GFX_Vector4()
                                ThickMiddle = unpackFloat32()
                                ThickInner = unpackFloat32()
                                ThickSmooth = unpackFloat32()
                                ShvNbFrames = unpackInt32()
                                lenPartsScale = unpackUInt32()
                                PartsScale = []

                                for x in range(lenPartsScale):
                                    value = unpackFloat32()
                                    PartsScale.append(value)

                                HalftoneFactor = unpackFloat32()
                                HalftoneCutoutLevels = unpackFloat32()
                                UVBlackoutFactor = unpackFloat32()
                                UVBlackoutDesaturation = unpackFloat32()
                                UVBlackoutContrast = unpackFloat32()
                                UVBlackoutBrightness = unpackFloat32()
                                UVBlackoutColor = GFX_Vector4()
                                ToonFactor = unpackFloat32()
                                ToonCutoutLevels = unpackFloat32()
                                lenPlayersProps = unpackUInt32()
                                PlayersProps = []

                                for x in range(lenPlayersProps):
                                    value = unpackFloat32()
                                    PlayersProps.append(value)

                                RefractionFactor = unpackFloat32()
                                RefractionTint = GFX_Vector4()
                                RefractionScale = GFX_Vector4()
                                RefractionOpacity = unpackFloat32()
                                ColoredShivaThresholds = GFX_Vector4()
                                ColoredShivaColor0 = GFX_Vector4()
                                ColoredShivaColor1 = GFX_Vector4()
                                ColoredShivaColor2 = GFX_Vector4()
                                SaturationModifier = unpackFloat32()
                                SlimeFactor = unpackFloat32()
                                SlimeColor = GFX_Vector4()
                                SlimeOpacity = unpackFloat32()
                                SlimeAmbient = unpackFloat32()
                                limeNormalTiling = unpackFloat32()
                                SlimeLightAngle = unpackFloat32()
                                SlimeRefraction = unpackFloat32()
                                SlimeRefractionIndex = unpackFloat32()
                                SlimeSpecular = unpackFloat32()
                                SlimeSpecularPower = unpackFloat32()
                                OverlayBlendFactor = unpackFloat32()
                                OverlayBlendColor = GFX_Vector4()
                                BackgroundSobelFactor = unpackFloat32()
                                BackgroundSobelColor = GFX_Vector4()
                                PlayerGlowFactor = unpackFloat32()
                                PlayerGlowColor = GFX_Vector4()
                                lenSwapHeadWithPlayer = unpackUInt32()
                                SwapHeadWithPlayer = []

                                for x in range(lenSwapHeadWithPlayer):
                                    value = unpackUInt32()
                                    SwapHeadWithPlayer.append(value)

                                lenAnimatePlayerHead = unpackUInt32()
                                AnimatePlayerHead = []

                                for x in range(lenAnimatePlayerHead):
                                    value = unpackUInt32()
                                    AnimatePlayerHead.append(value)

                                AnimatedHeadTotalTime = unpackFloat32()
                                AnimatedHeadRestTime = unpackFloat32()
                                AnimatedHeadFrameTime = unpackFloat32()
                                AnimatedHeadMaxDistance = unpackFloat32()
                                AnimatedHeadMaxAngle = unpackFloat32()
                                ScreenBlendInverseAlphaFactor = unpackFloat32()
                                ScreenBlendInverseAlphaScaleX = unpackFloat32()
                                ScreenBlendInverseAlphaScaleY = unpackFloat32()
                                ScreenBlendInverseAlphaTransX = unpackFloat32()
                                ScreenBlendInverseAlphaTransY = unpackFloat32()
                                TintMulColorFactor = unpackFloat32()
                                TintMulColor = GFX_Vector4()
                                FloorPlaneFactor = unpackFloat32()
                                FloorPlaneTiles = GFX_Vector4()
                                FloorSpeedX = unpackFloat32()
                                FloorSpeedY = unpackFloat32()
                                FloorWaveSpeed = unpackFloat32()
                                FloorBlendMode = unpackUInt32()
                                FloorPlaneImageID = unpackUInt32()
                                StartRadius = unpackFloat32()
                                EndRadius = unpackFloat32()
                                RadiusVariance = unpackFloat32()
                                RadiusNoiseRate = unpackFloat32()
                                RadiusNoiseAmp = unpackFloat32()
                                MinSpin = unpackFloat32()
                                MaxSpin = unpackFloat32()
                                DirAngle = unpackFloat32()
                                MinWanderRate = unpackFloat32()
                                MaxWanderRate = unpackFloat32()
                                MinWanderAmp = unpackFloat32()
                                MaxWanderAmp = unpackFloat32()
                                MinSpeed = unpackFloat32()
                                MaxSpeed = unpackFloat32()
                                MotionPower = unpackFloat32()
                                Amount = unpackFloat32()
                                ImageID = unpackUInt32()
                                StartR = unpackFloat32()
                                StartG = unpackFloat32()
                                StartB = unpackFloat32()
                                EndR = unpackFloat32()
                                EndG = unpackFloat32()
                                EndB = unpackFloat32()
                                StartAlpha = unpackFloat32()
                                EndAlpha = unpackFloat32()
                                TexturedOutlineFactor = unpackFloat32()
                                TexturedOutlineTiling = unpackFloat32()
                                TripleLayerBackgroundFactor = unpackFloat32()
                                TripleLayerBackgroundTintColor = GFX_Vector4()
                                TripleLayerBackgroundSpeedX = unpackFloat32()
                                TripleLayerBackgroundSpeedY = unpackFloat32()
                                TrailEffectId = unpackUInt32()

                                return {
                                    "__class": "AutoDanceFxDesc",
                                    "Opacity": beautifyFloat(Opacity),
                                    "ColorLow": beautifyFloat(ColorLow),
                                    "ColorMid": beautifyFloat(ColorMid),
                                    "ColorHigh": beautifyFloat(ColorHigh),
                                    "LowToMid": beautifyFloat(LowToMid),
                                    "LowToMidWidth": beautifyFloat(LowToMidWidth),
                                    "MidToHigh": beautifyFloat(MidToHigh),
                                    "MidToHighWidth": beautifyFloat(MidToHighWidth),
                                    "SobColor": beautifyFloat(SobColor),
                                    "OutColor": beautifyFloat(OutColor),
                                    "ThickMiddle": beautifyFloat(ThickMiddle),
                                    "ThickInner": beautifyFloat(ThickInner),
                                    "ThickSmooth": beautifyFloat(ThickSmooth),
                                    "ShvNbFrames": ShvNbFrames,
                                    "PartsScale": list(PartsScale),
                                    "HalftoneFactor": beautifyFloat(HalftoneFactor),
                                    "HalftoneCutoutLevels": beautifyFloat(HalftoneCutoutLevels),
                                    "UVBlackoutFactor": beautifyFloat(UVBlackoutFactor),
                                    "UVBlackoutDesaturation": beautifyFloat(UVBlackoutDesaturation),
                                    "UVBlackoutContrast": beautifyFloat(UVBlackoutContrast),
                                    "UVBlackoutBrightness": beautifyFloat(UVBlackoutBrightness),
                                    "UVBlackoutColor": beautifyFloat(UVBlackoutColor),
                                    "ToonFactor": beautifyFloat(ToonFactor),
                                    "ToonCutoutLevels": beautifyFloat(ToonCutoutLevels),
                                    "PlayersProps": list(PlayersProps),
                                    "RefractionFactor": beautifyFloat(RefractionFactor),
                                    "RefractionTint": beautifyFloat(RefractionTint),
                                    "RefractionScale": beautifyFloat(RefractionScale),
                                    "RefractionOpacity": beautifyFloat(RefractionOpacity),
                                    "ColoredShivaThresholds": beautifyFloat(ColoredShivaThresholds),
                                    "ColoredShivaColor0": beautifyFloat(ColoredShivaColor0),
                                    "ColoredShivaColor1": beautifyFloat(ColoredShivaColor1),
                                    "ColoredShivaColor2": beautifyFloat(ColoredShivaColor2),
                                    "SaturationModifier": beautifyFloat(SaturationModifier),
                                    "SlimeFactor": beautifyFloat(SlimeFactor),
                                    "SlimeColor": beautifyFloat(SlimeColor),
                                    "SlimeOpacity": beautifyFloat(SlimeOpacity),
                                    "SlimeAmbient": beautifyFloat(SlimeAmbient),
                                    "SlimeNormalTiling": beautifyFloat(limeNormalTiling),
                                    "SlimeLightAngle": beautifyFloat(SlimeLightAngle),
                                    "SlimeRefraction": beautifyFloat(SlimeRefraction),
                                    "SlimeRefractionIndex": beautifyFloat(SlimeRefractionIndex),
                                    "SlimeSpecular": beautifyFloat(SlimeSpecular),
                                    "SlimeSpecularPower": beautifyFloat(SlimeSpecularPower),
                                    "OverlayBlendFactor": beautifyFloat(OverlayBlendFactor),
                                    "OverlayBlendColor": beautifyFloat(OverlayBlendColor),
                                    "BackgroundSobelFactor": beautifyFloat(BackgroundSobelFactor),
                                    "BackgroundSobelColor": beautifyFloat(BackgroundSobelColor),
                                    "PlayerGlowFactor": beautifyFloat(PlayerGlowFactor),
                                    "PlayerGlowColor": beautifyFloat(PlayerGlowColor),
                                    "SwapHeadWithPlayer": list(SwapHeadWithPlayer),
                                    "AnimatePlayerHead": list(AnimatePlayerHead),
                                    "AnimatedHeadTotalTime": beautifyFloat(AnimatedHeadTotalTime),
                                    "AnimatedHeadRestTime": beautifyFloat(AnimatedHeadRestTime),
                                    "AnimatedHeadFrameTime": beautifyFloat(AnimatedHeadFrameTime),
                                    "AnimatedHeadMaxDistance": beautifyFloat(AnimatedHeadMaxDistance),
                                    "AnimatedHeadMaxAngle": beautifyFloat(AnimatedHeadMaxAngle),
                                    "ScreenBlendInverseAlphaFactor": beautifyFloat(ScreenBlendInverseAlphaFactor),
                                    "ScreenBlendInverseAlphaScaleX": beautifyFloat(ScreenBlendInverseAlphaScaleX),
                                    "ScreenBlendInverseAlphaScaleY": beautifyFloat(ScreenBlendInverseAlphaScaleY),
                                    "ScreenBlendInverseAlphaTransX": beautifyFloat(ScreenBlendInverseAlphaTransX),
                                    "ScreenBlendInverseAlphaTransY": beautifyFloat(ScreenBlendInverseAlphaTransY),
                                    "TintMulColorFactor": beautifyFloat(TintMulColorFactor),
                                    "TintMulColor": beautifyFloat(TintMulColor),
                                    "FloorPlaneFactor": beautifyFloat(FloorPlaneFactor),
                                    "FloorPlaneTiles": beautifyFloat(FloorPlaneTiles),
                                    "FloorSpeedX": beautifyFloat(FloorSpeedX),
                                    "FloorSpeedY": beautifyFloat(FloorSpeedY),
                                    "FloorWaveSpeed": beautifyFloat(FloorWaveSpeed),
                                    "FloorBlendMode": FloorBlendMode,
                                    "FloorPlaneImageID": FloorPlaneImageID,
                                    "StartRadius": beautifyFloat(StartRadius),
                                    "EndRadius": beautifyFloat(EndRadius),
                                    "RadiusVariance": beautifyFloat(RadiusVariance),
                                    "RadiusNoiseRate": beautifyFloat(RadiusNoiseRate),
                                    "RadiusNoiseAmp": beautifyFloat(RadiusNoiseAmp),
                                    "MinSpin": beautifyFloat(MinSpin),
                                    "MaxSpin": beautifyFloat(MaxSpin),
                                    "DirAngle": beautifyFloat(DirAngle),
                                    "MinWanderRate": beautifyFloat(MinWanderRate),
                                    "MaxWanderRate": beautifyFloat(MaxWanderRate),
                                    "MinWanderAmp": beautifyFloat(MinWanderAmp),
                                    "MaxWanderAmp": beautifyFloat(MaxWanderAmp),
                                    "MinSpeed": beautifyFloat(MinSpeed),
                                    "MaxSpeed": beautifyFloat(MaxSpeed),
                                    "MotionPower": beautifyFloat(MotionPower),
                                    "Amount": beautifyFloat(Amount),
                                    "ImageID": ImageID,
                                    "StartR": beautifyFloat(StartR),
                                    "StartG": beautifyFloat(StartG),
                                    "StartB": beautifyFloat(StartB),
                                    "EndR": beautifyFloat(EndR),
                                    "EndG": beautifyFloat(EndG),
                                    "EndB": beautifyFloat(EndB),
                                    "StartAlpha": beautifyFloat(StartAlpha),
                                    "EndAlpha": beautifyFloat(EndAlpha),
                                    "TexturedOutlineFactor": beautifyFloat(TexturedOutlineFactor),
                                    "TexturedOutlineTiling": beautifyFloat(TexturedOutlineTiling),
                                    "TripleLayerBackgroundFactor": beautifyFloat(TripleLayerBackgroundFactor),
                                    "TripleLayerBackgroundTintColor": beautifyFloat(TripleLayerBackgroundTintColor),
                                    "TripleLayerBackgroundSpeedX": beautifyFloat(TripleLayerBackgroundSpeedX),
                                    "TripleLayerBackgroundSpeedY": beautifyFloat(TripleLayerBackgroundSpeedY),
                                    "TrailEffectId": TrailEffectId
                                }

                            def effect_events():
                                lenEffect_events = unpackUInt32()
                                effect_events = []

                                for x in range(lenEffect_events):
                                    byte.read(4)
                                    StartTime = unpackFloat32()
                                    Duration = unpackFloat32()

                                    dummyFxEvent = {
                                        "__class": "FxEvent",
                                        "StartTime": beautifyFloat(StartTime),
                                        "Duration": beautifyFloat(Duration)
                                    }

                                    effect_events.append(dummyFxEvent)

                                return effect_events

                            dummyAutodanceVideoStructure["background_effect"] = AutoDanceFxDesc()
                            dummyAutodanceVideoStructure["background_effect_events"] = effect_events()
                            dummyAutodanceVideoStructure["player_effect"] = AutoDanceFxDesc()
                            dummyAutodanceVideoStructure["player_effect_events"] = effect_events()

                            lenProp_events = unpackUInt32()
                            prop_events = []

                            for x in range(lenProp_events):
                                byte.read(4)
                                StartTime = unpackFloat32()
                                Duration = unpackFloat32()
                                lenAssociatedProps = unpackUInt32()
                                AssociatedProps = []

                                for x in range(lenAssociatedProps):
                                    value = unpackUInt32()
                                    AssociatedProps.append(value)

                                dummyPropEvent = {
                                    "__class": "PropEvent",
                                    "StartTime": beautifyFloat(StartTime),
                                    "Duration": beautifyFloat(Duration),
                                    "AssociatedProps": AssociatedProps
                                }

                                prop_events.append(dummyPropEvent)

                            dummyAutodanceVideoStructure["prop_events"] = prop_events

                            lenProps = unpackUInt32()
                            props = []

                            for x in range(lenProps):
                                byte.read(4)
                                Index = unpackInt32()
                                PivotX = unpackFloat32()
                                PivotY = unpackFloat32()
                                Size = unpackFloat32()
                                PropPart = unpackUInt32()

                                dummyAutodancePropData = {
                                    "__class": "AutodancePropData",
                                    "Index": Index,
                                    "PivotX": beautifyFloat(PivotX),
                                    "PivotY": beautifyFloat(PivotY),
                                    "Size": beautifyFloat(Size),
                                    "fx_assetID": "",
                                    "PropPart": PropPart
                                }

                                props.append(dummyAutodancePropData)

                            dummyAutodanceVideoStructure["props"] = props

                            lenProps_players_config = unpackUInt32()
                            props_players_config = []

                            for x in range(lenProps):
                                byte.read(4)
                                Index = unpackInt32()
                                lenActiveProps = unpackUInt32()
                                ActiveProps = []

                                for x in range(lenActiveProps):
                                    value = unpackUInt32()
                                    ActiveProps.append(value)

                                dummyPropPlayerConfig = {
                                    "__class": "PropPlayerConfig",
                                    "Index": Index,
                                    "ActiveProps": ActiveProps
                                }

                                props_players_config.append(dummyPropPlayerConfig)

                            dummyAutodanceVideoStructure["props_players_config"] = props_players_config

                            autodanceSoundPath = unpackLongPath()
                            dummyAutodanceData["autodanceSoundPath"] = autodanceSoundPath.replace("jd2015", "maps") if mapsPath == "y" else autodanceSoundPath
                            dummyAutodanceData["video_structure"] = dummyAutodanceVideoStructure
                            dummyAutodanceData["recording_structure"] = dummyAutodanceRecordingStructure
                            dummyCOMPONENT["autodanceData"] = dummyAutodanceData
                            dummyActor_Template["COMPONENTS"].append(dummyCOMPONENT)

                        elif strCOMPONENT == "JD_BlockFlowTemplate":
                            byte.read(4)
                            IsMashUp = unpackUInt32()
                            IsPartyMaster = unpackUInt32()

                            if IsMashUp == 1:
                                print(f"---------- Detected type: MashUp")

                            if IsPartyMaster == 1:
                                print(f"---------- Detected type: PartyMaster")

                            lenBlockDescriptorVector = unpackUInt32()

                            dummyCOMPONENT = {
                                "__class": strCOMPONENT,
                                "IsMashUp": IsMashUp,
                                "IsPartyMaster": IsPartyMaster,
                                "BlockDescriptorVector": []
                            }

                            for x in range(lenBlockDescriptorVector):
                                byte.read(8)
                                songName = unpackStr8()
                                frstBeat = unpackUInt32()
                                lastBeat = unpackUInt32()
                                songSwitch = unpackUInt32()
                                videoCoachOffset = unpackFloat32(), unpackFloat32()
                                videoCoachScale = unpackFloat32()
                                danceStepName = unpackStr8()
                                playingSpeed = unpackFloat32()
                                isEntryPoint = unpackUInt32()
                                isEmptyBlock = unpackUInt32()
                                isNoScoreBlock = unpackUInt32()
                                guid = unpackStr8()
                                lenAlternativeBlocks = unpackUInt32()

                                dummyBlockReplacements = {
                                    "__class": "JD_BlockReplacements",
                                    "BaseBlock": {
                                        "__class": "JD_BlockDescriptor",
                                        "songName": songName,
                                        "frstBeat": frstBeat,
                                        "lastBeat": lastBeat,
                                        "songSwitch": songSwitch,
                                        "videoCoachOffset": beautifyFloat(list(videoCoachOffset)),
                                        "videoCoachScale": beautifyFloat(videoCoachScale),
                                        "danceStepName": danceStepName,
                                        "playingSpeed": beautifyFloat(playingSpeed),
                                        "isEntryPoint": isEntryPoint,
                                        "isEmptyBlock": isEmptyBlock,
                                        "isNoScoreBlock": isNoScoreBlock,
                                        "guid": guid,
                                        "forceDisplayLastPictos": 0
                                    },
                                    "AlternativeBlocks": []
                                }

                                for x in range(lenAlternativeBlocks):
                                    byte.read(4)
                                    songName = unpackStr8()
                                    frstBeat = unpackUInt32()
                                    lastBeat = unpackUInt32()
                                    songSwitch = unpackUInt32()
                                    videoCoachOffset = struct.unpack(">ff", byte.read(8))
                                    videoCoachScale = unpackFloat32()
                                    danceStepName = unpackStr8()
                                    playingSpeed = unpackFloat32()
                                    isEntryPoint = unpackUInt32()
                                    isEmptyBlock = unpackUInt32()
                                    isNoScoreBlock = unpackUInt32()
                                    guid = unpackStr8()

                                    dummyAlternativeBlocks = {
                                        "__class": "JD_BlockDescriptor",
                                        "songName": songName,
                                        "frstBeat": frstBeat,
                                        "lastBeat": lastBeat,
                                        "songSwitch": songSwitch,
                                        "videoCoachOffset": beautifyFloat(list(videoCoachOffset)),
                                        "videoCoachScale": beautifyFloat(videoCoachScale),
                                        "danceStepName": danceStepName,
                                        "playingSpeed": beautifyFloat(playingSpeed),
                                        "isEntryPoint": isEntryPoint,
                                        "isEmptyBlock": isEmptyBlock,
                                        "isNoScoreBlock": isNoScoreBlock,
                                        "guid": guid,
                                        "forceDisplayLastPictos": 0
                                    }

                                    dummyBlockReplacements["AlternativeBlocks"].append(dummyAlternativeBlocks)
                                dummyCOMPONENT["BlockDescriptorVector"].append(dummyBlockReplacements)
                            dummyActor_Template["COMPONENTS"].append(dummyCOMPONENT)

                        elif strCOMPONENT == "JD_SongDescTemplate":
                            structSize = unpackUInt32()
                            MapName = unpackStr8()
                            JDVersion = unpackInt32()
                            OriginalJDVersion = unpackInt32()
                            lenRelatedAlbums = unpackUInt32()

                            RelatedAlbums = []
                            for x in range(lenRelatedAlbums):
                                RelatedAlbum = unpackStr8()
                                RelatedAlbums.append(RelatedAlbum)

                            lenGameModes = unpackUInt32()

                            firstGameModeDesc = []
                            for x in range(lenGameModes):
                                structSize = unpackUInt32()
                                Mode = unpackUInt32()
                                Flags = unpackUInt32()
                                NumCoach = unpackUInt32()
                                LocaleID = unpackUInt32()
                                Status = unpackInt32()
                                Mojo_value = unpackUInt32()
                                Colors = unpackInt32()
                                Config_template = unpackLongPath()
                                CountInProgression = unpackInt32()

                                if x == 0:
                                    firstGameModeDesc.append({
                                        "__class": "GameModeDesc",
                                        "Mode": Mode,
                                        "Flags": Flags,
                                        "NumCoach": NumCoach,
                                        "LocaleID": LocaleID,
                                        "Status": Status,
                                        "Mojo_value": Mojo_value,
                                        "Colors": Colors,
                                        "Config_template": Config_template,
                                        "CountInProgression": CountInProgression
                                    })

                            Artist = unpackStr8()
                            DancerName = unpackStr8()
                            Title = unpackStr8()
                            NumCoach = unpackUInt32()
                            MainCoach = unpackInt32()
                            Difficulty = unpackUInt32()
                            backgroundType = unpackUInt32()
                            LyricsType = unpackInt32()
                            Energy = unpackUInt32()
                            AudioPreviewFadeTime = unpackFloat32()

                            dummyCOMPONENT = {
                                "__class": strCOMPONENT,
                                "MapName": MapName,
                                "JDVersion": 2016,
                                "OriginalJDVersion": 2015,
                                "RelatedAlbums": RelatedAlbums,
                                "Artist": Artist,
                                "DancerName": DancerName,
                                "Title": Title,
                                "Credits": "Empty Credits",
                                "PhoneImages": {},
                                "NumCoach": NumCoach,
                                "MainCoach": MainCoach,
                                "Difficulty": Difficulty,
                                "backgroundType": backgroundType,
                                "LyricsType": LyricsType,
                                "Energy": Energy,
                                "Tags": ["Main"],
                                "Status": firstGameModeDesc[0]["Status"],
                                "LocaleID": firstGameModeDesc[0]["LocaleID"],
                                "MojoValue": firstGameModeDesc[0]["Mojo_value"],
                                "CountInProgression": firstGameModeDesc[0]["CountInProgression"],
                                "DefaultColors": {},
                                "Paths": {
                                    "Avatars": None,
                                    "AsyncPlayers": None
                                }
                            }

                            lenAudioPreviews = unpackUInt32()
                            for i in range(lenAudioPreviews):
                                structSize = unpackUInt32()
                                nameKey = unpackUInt32()
                                Startbeat = unpackInt32()
                                Endbeat = unpackInt32()

                            lenDefaultColors = unpackUInt32()
                            DefaultColors = {}
                            for i in range(lenDefaultColors):
                                enumColorsKey = {
                                    835957575: "lyrics",
                                    2631470027: "theme"
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
                            for i in range(lenAvatars):
                                filePath = unpackLongPath()

                            lenAsyncPlayers = unpackUInt32()
                            for i in range(lenAsyncPlayers):
                                filePath = unpackLongPath()

                            if 1 <= NumCoach <= 4:
                                dummyCOMPONENT["PhoneImages"] = {
                                    "Cover": f"world/maps/{MapName.lower()}/menuart/textures/{MapName.lower()}_cover_phone.jpg",
                                    "coach1": f"world/maps/{MapName.lower()}/menuart/textures/{MapName.lower()}_coach_1_phone.png",
                                }
                                for x in range(2, NumCoach + 1):
                                    dummyCOMPONENT["PhoneImages"][f"coach{x}"] = f"world/maps/{MapName.lower()}/menuart/textures/{MapName.lower()}_coach_{x}_phone.png"

                                keyOrder = ["Cover", "coach3", "coach2", "coach4", "coach1"]

                                dummyCOMPONENT["PhoneImages"] = {
                                    key: dummyCOMPONENT["PhoneImages"][key]
                                    for key in keyOrder
                                    if key in dummyCOMPONENT["PhoneImages"]
                                }

                            else:
                                print("\033[31m---------- Can't create 'PhoneImages' keys!\033[0m")

                            dummyActor_Template["COMPONENTS"].append(dummyCOMPONENT)

                        elif strCOMPONENT in ("MasterTape_Template", "TapeCase_Template"):
                            structSize = unpackUInt32()
                            lenTapesRack = unpackUInt32()
                            TapesRack = []

                            for x in range(lenTapesRack):
                                structSize = unpackUInt32()
                                lenEntries = unpackUInt32()
                                Entries = []

                                for x in range(lenEntries):
                                    structSize = unpackUInt32()
                                    Label = byte.read(4)

                                    if Label in hashesDictionary.Hashes:
                                        strLabel = hashesDictionary.Hashes[Label]
                                        print(f"---------- Detected Label: {strLabel}")

                                    else:
                                        print(f"\033[33m---------- No Label detected!\033[0m")
                                        strLabel = None
                                        continue

                                    Path = unpackLongPath()

                                    dummyTapeEntry = {
                                        "__class": "TapeEntry",
                                        "Label": strLabel,
                                        "Path": Path.replace("jd2015", "maps") if mapsPath == "y" else Path
                                    }

                                    Entries.append(dummyTapeEntry)

                                dummyTapeGroup = {
                                    "__class": "TapeGroup",
                                    "Entries": Entries
                                }

                                TapesRack.append(dummyTapeGroup)

                            dummyCOMPONENT = {
                                "__class": strCOMPONENT,
                                "TapesRack": TapesRack
                            }

                            dummyActor_Template["COMPONENTS"].append(dummyCOMPONENT)

                        elif strCOMPONENT == "MusicTrackComponent_Template":
                            structSize = unpackUInt32()
                            MusicTrackData = unpackUInt32()
                            MusicTrackStructure = unpackUInt32()
                            lenMarkers = unpackUInt32()

                            dummyCOMPONENT = {
                                "__class": strCOMPONENT,
                                "trackData": {
                                    "__class": "MusicTrackData",
                                    "structure": {
                                        "__class": "MusicTrackStructure",
                                        "markers": [],
                                        "signatures": [],
                                        "sections": [],
                                        "startBeat": 0,
                                        "endBeat": 0,
                                        "videoStartTime": 0,
                                        "previewEntry": 0,
                                        "previewLoopStart": 0,
                                        "previewLoopEnd": 50,
                                        "volume": 0,
                                        "entryPoints": []
                                    },
                                    "path": "",
                                    "url": ""
                                }
                            }

                            markers = []
                            for x in range(lenMarkers):
                                marker = unpackInt32()
                                markers.append(marker)

                            dummyCOMPONENT["trackData"]["structure"]["markers"] = markers
                            lenSignatures = unpackUInt32()

                            for x in range(lenSignatures):
                                byte.read(4)
                                marker = unpackInt32()
                                beats = unpackInt32()
                                dummyMusicSignature = {
                                    "__class": "MusicSignature",
                                    "marker": marker,
                                    "beats": beats
                                }
                                dummyCOMPONENT["trackData"]["structure"]["signatures"].append(dummyMusicSignature)

                            lenSections = unpackUInt32()

                            for x in range(lenSections):
                                byte.read(4)
                                marker = unpackInt32()
                                sectionType = unpackInt32()
                                comment = unpackStr8()

                                dummyMusicSection = {
                                    "__class": "MusicSection",
                                    "marker": marker,
                                    "sectionType": sectionType,
                                    "comment": comment
                                }
                                dummyCOMPONENT["trackData"]["structure"]["sections"].append(dummyMusicSection)

                            startBeat = unpackInt32()
                            endBeat = unpackInt32()
                            videoStartTime = unpackFloat32()
                            lenEntryPoints = unpackUInt32()
                            entryPoints = []

                            for x in range(lenEntryPoints):
                                value = unpackInt32()
                                entryPoints.append(value)

                            path = unpackLongPath()
                            volume = unpackFloat32()

                            dummyCOMPONENT["trackData"]["structure"]["startBeat"] = startBeat
                            dummyCOMPONENT["trackData"]["structure"]["endBeat"] = endBeat
                            dummyCOMPONENT["trackData"]["structure"]["videoStartTime"] = beautifyFloat(videoStartTime)
                            dummyCOMPONENT["trackData"]["structure"]["volume"] = beautifyFloat(volume)
                            dummyCOMPONENT["trackData"]["structure"]["entryPoints"] = entryPoints
                            dummyCOMPONENT["trackData"]["path"] = path.replace("jd2015", "maps") if mapsPath == "y" else path
                            dummyActor_Template["COMPONENTS"].append(dummyCOMPONENT)

                        elif strCOMPONENT == "SoundComponent_Template":
                            byte.read(12)
                            name = byte.read(4)

                            if name in hashesDictionary.Hashes:
                                strName = hashesDictionary.Hashes[name].upper()
                                print(f"---------- Detected name: {strName}")
                                if strName == "NULL":
                                    strName = ""
                            else:
                                if inputFile.endswith(".tpl.ckd"):
                                    rootFileName = inputFile[:-len(".tpl.ckd")]

                                strName = rootFileName.upper()
                                print(f"---------- No name detected --> using file name: {strName}")

                            volume = unpackFloat32()
                            category = byte.read(4)

                            if category in hashesDictionary.Hashes:
                                strCategory = hashesDictionary.Hashes[category].upper()
                                print(f"---------- Detected category: {strCategory}")
                                if strCategory == "NULL":
                                    strCategory = ""
                            else:
                                strCategory = ""

                            limitCategory = byte.read(4)

                            if limitCategory in hashesDictionary.Hashes:
                                strLimitCategory = hashesDictionary.Hashes[limitCategory].upper()
                                if strLimitCategory == "NULL":
                                    strLimitCategory = ""
                            else:
                                strLimitCategory = ""

                            limitMode = unpackUInt32()
                            maxInstances = unpackUInt32()
                            isStream = unpackInt32()
                            isPrefetched = unpackInt32()
                            lenFiles = unpackUInt32()
                            files = []

                            for x in range(lenFiles):
                                file = unpackLongPath()
                                files.append(file.replace("jd2015", "maps") if mapsPath == "y" else file)

                            lenFilesIntro = unpackUInt32()
                            filesIntro = []

                            for x in range(lenFilesIntro):
                                fileIntro = unpackLongPath()
                                filesIntro.append(fileIntro.replace("jd2015", "maps") if mapsPath == "y" else fileIntro)

                            lenFilesBody = unpackUInt32()
                            filesBody = []

                            for x in range(lenFilesBody):
                                fileBody = unpackLongPath()
                                filesBody.append(fileBody.replace("jd2015", "maps") if mapsPath == "y" else fileBody)

                            lenFilesOutro = unpackUInt32()
                            filesOutro = []

                            for x in range(lenFilesOutro):
                                fileOutro = unpackLongPath()
                                filesOutro.append(fileOutro.replace("jd2015", "maps") if mapsPath == "y" else fileOutro)

                            serialPlayingMode = unpackUInt32()
                            serialStoppingMode = unpackUInt32()
                            params = byte.read(4)
                            numChannels = unpackUInt32()
                            loop = unpackUInt32()
                            playMode = unpackUInt32()
                            playModeInput = byte.read(4)

                            if playModeInput in hashesDictionary.Hashes:
                                lenPlayModeInput = hashesDictionary.Hashes[playModeInput].upper()
                                if lenPlayModeInput == "NULL":
                                    lenPlayModeInput = ""
                            else:
                                lenPlayModeInput = ""

                            randomVolMin = unpackFloat32()
                            randomVolMax = unpackFloat32()
                            delay = unpackFloat32()
                            randomDelay = unpackFloat32()
                            randomPitchMin = unpackFloat32()
                            randomPitchMax = unpackFloat32()
                            fadeInTime = unpackFloat32()
                            fadeOutTime = unpackFloat32()
                            filterFrequency = unpackFloat32()
                            filterType = unpackUInt32()
                            metronomeType = unpackUInt32()
                            playOnNext = unpackUInt32()
                            playOnNextTransition = unpackFloat32()
                            transitionSampleOffset = unpackUInt32()

                            lenModifiers = unpackUInt32()
                            modifiers = []

                            for x in range(lenModifiers):
                                modifier = unpackUInt32()
                                modifiers.append(modifier)

                            pauseInsensitiveFlags = unpackUInt32()
                            outDevices = unpackUInt32()
                            soundPlayAfterdestroy = unpackUInt32()

                            dummyCOMPONENT = {
                                "__class": strCOMPONENT,
                                "soundList": [{
                                        "__class": "SoundDescriptor_Template",
                                        "name": strName,
                                        "volume": beautifyFloat(volume),
                                        "category": strCategory,
                                        "limitCategory": strLimitCategory,
                                        "limitMode": limitMode,
                                        "maxInstances": maxInstances,
                                        "files": files,
                                        "filesIntro": filesIntro,
                                        "filesBody": filesBody,
                                        "filesOutro": filesOutro,
                                        "serialPlayingMode": serialPlayingMode,
                                        "serialStoppingMode": serialStoppingMode,
                                        "params": {
                                            "__class": "SoundParams",
                                            "loop": loop,
                                            "playMode": playMode,
                                            "playModeInput": lenPlayModeInput,
                                            "randomVolMin": beautifyFloat(randomVolMin),
                                            "randomVolMax": beautifyFloat(randomVolMax),
                                            "delay": beautifyFloat(delay),
                                            "randomDelay": beautifyFloat(randomDelay),
                                            "randomPitchMin": beautifyFloat(randomPitchMin),
                                            "randomPitchMax": beautifyFloat(randomPitchMax),
                                            "fadeInTime": beautifyFloat(fadeInTime),
                                            "fadeOutTime": beautifyFloat(fadeOutTime),
                                            "filterFrequency": beautifyFloat(filterFrequency),
                                            "filterType": filterType,
                                            "modifiers": modifiers
                                        },
                                        "pauseInsensitiveFlags": pauseInsensitiveFlags,
                                        "outDevices": outDevices,
                                        "soundPlayAfterdestroy": soundPlayAfterdestroy
                                    }]
                            }

                            dummyActor_Template["COMPONENTS"].append(dummyCOMPONENT)

                        else:
                            print(f"\033[31m------ THERE'S AN ERROR WITH A COMPONENT\033[0m")
                            continue

                    else:
                        print(f"\033[31m---- ERROR\033[0m")
                        continue

            cleaningLists(dummyActor_Template)
            inputFileRelativePath = os.path.relpath(inputFilePath, "input")
            outputPath = os.path.join(remakeFormat, inputFileRelativePath)
            os.makedirs(os.path.dirname(outputPath), exist_ok=True)
            with open(outputPath, "w", encoding="utf-8") as s:
                json.dump(dummyActor_Template, s, ensure_ascii=False, separators=(",", ":"))
                print(f"\033[32m-- Deserialized:\033[0m {inputFile}")
            with open(outputPath, "ab") as f:
                f.write(b'\x00')