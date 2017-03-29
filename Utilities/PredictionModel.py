


class PredictionModel:


    def GetDataStorage(self, cwpbn, beams, deployment_duration, cei,
                       is_e0000001,
                       is_e0000002,
                       is_e0000003,
                       is_e0000004,
                       is_e0000005,
                       is_e0000006,
                       is_e0000007,
                       is_e0000008,
                       is_e0000009,
                       is_e0000010,
                       is_e0000011,
                       is_e0000012,
                       is_e0000013,
                       is_e0000014,
                       is_e0000015):

        e0000001 = 0
        if is_e0000001:
            e0000001 = 4 * (cwpbn * beams + 7)

        e0000002 = 0
        if is_e0000002:
            e0000002 = 4 * (cwpbn * beams + 7)

        e0000003 = 0
        if is_e0000003:
            e0000003 = 4 * (cwpbn * beams + 7)

        e0000004 = 0
        if is_e0000004:
            e0000004 = 4 * (cwpbn * beams + 7)

        e0000005 = 0
        if is_e0000005:
            e0000005 = 4 * (cwpbn * beams + 7)

        e0000006 = 0
        if is_e0000006:
            e0000006 = 4 * (cwpbn * beams + 7)

        e0000007 = 0
        if is_e0000007:
            e0000007 = 4 * (cwpbn * beams + 7)

        e0000008 = 0
        if is_e0000008:
            e0000008 = 4 * (23 + 7)

        e0000009 = 0
        if is_e0000009:
            e0000009 = 4 * (19 + 7)

        e0000010 = 0
        if is_e0000010:
            e0000010 = 4 * (14 + 15 * beams + 7)

        e0000011 = 0
        if is_e0000011:
            e0000011 = 0

        e0000012 = 0
        if is_e0000012:
            e0000012 = 4 * (23 + 7)

        e0000013 = 0
        if is_e0000013:
            e0000013 = 4 * (30 + 7)

        e0000014 = 0
        if is_e0000014:
            e0000014 = 4 * (23 + 7)

        e0000015 = 0
        if is_e0000015:
            e0000015 = 4 * (8 * beams + 1 + 7)

        bytes_per_ensemble = e0000001 + e0000002 + e0000003 + e0000004 + e0000005 + e0000006 + e0000007 + e0000008 + e0000009 + e0000010 + e0000011 + e0000012 + e0000013 + e0000014 + e0000015;
        checksum = 4
        wrapper = 32   # Header

        ensemble_size = bytes_per_ensemble + checksum + wrapper;

        ensembles = deployment_duration * 24 * 3600 / cei

        return ensembles * ensemble_size
