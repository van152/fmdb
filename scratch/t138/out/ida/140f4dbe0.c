__int64 __fastcall sub_140F4DBE0(
        __int64 a1,
        _QWORD *a2,
        unsigned int a3,
        char a4,
        __int16 *a5,
        void (__fastcall *a6)(_QWORD))
{
  _DWORD *v6; // rdi
  __int64 v11; // rbp
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  void (__fastcall ***v13)(_QWORD, __int64); // rcx
  _DWORD *v14; // rcx
  __int64 v15; // rsi
  __int64 v16; // rcx
  __int64 v17; // rax
  _DWORD *v18; // rax
  __int64 v19; // rcx
  __int64 v20; // rbp
  void (__fastcall ***v21)(_QWORD, __int64); // rcx
  void (__fastcall ***v22)(_QWORD, __int64); // rcx
  _DWORD *v23; // rcx
  __int64 v24; // rbp
  void (__fastcall ***v25)(_QWORD, __int64); // rcx
  void (__fastcall ***v26)(_QWORD, __int64); // rcx
  _DWORD *v27; // rcx
  __int64 v28; // rbp
  void (__fastcall ***v29)(_QWORD, __int64); // rcx
  void (__fastcall ***v30)(_QWORD, __int64); // rcx
  _DWORD *v31; // rcx
  __int64 v32; // rbp
  void (__fastcall ***v33)(_QWORD, __int64); // rcx
  void (__fastcall ***v34)(_QWORD, __int64); // rcx
  _DWORD *v35; // rcx
  __int64 v36; // rbp
  void (__fastcall ***v37)(_QWORD, __int64); // rcx
  void (__fastcall ***v38)(_QWORD, __int64); // rcx
  _DWORD *v39; // rcx
  __int64 v40; // rbp
  void (__fastcall ***v41)(_QWORD, __int64); // rcx
  void (__fastcall ***v42)(_QWORD, __int64); // rcx
  _DWORD *v43; // rcx
  __int64 v44; // rbp
  void (__fastcall ***v45)(_QWORD, __int64); // rcx
  void (__fastcall ***v46)(_QWORD, __int64); // rcx
  _DWORD *v47; // rcx
  __int64 v48; // rbp
  void (__fastcall ***v49)(_QWORD, __int64); // rcx
  void (__fastcall ***v50)(_QWORD, __int64); // rcx
  _DWORD *v51; // rcx
  int *v52; // rax
  __int64 v53; // rbp
  int v54; // eax
  __int64 v55; // rcx
  __int64 v56; // rcx
  void (__fastcall ***v57)(_QWORD, __int64); // rcx
  __int64 v58; // rbp
  void (__fastcall ***v59)(_QWORD, __int64); // rcx
  void (__fastcall ***v60)(_QWORD, __int64); // rcx
  _DWORD *v61; // rcx
  unsigned int v62; // eax
  char v63; // bl
  bool v64; // zf
  void (__fastcall ***v65)(_QWORD, __int64); // rcx
  int v67; // [rsp+28h] [rbp-130h]
  __int64 v68; // [rsp+38h] [rbp-120h]
  _DWORD *v69; // [rsp+40h] [rbp-118h] BYREF
  __int64 v70; // [rsp+48h] [rbp-110h] BYREF
  __int64 v71; // [rsp+50h] [rbp-108h] BYREF
  _QWORD *v72; // [rsp+58h] [rbp-100h]
  char v73[8]; // [rsp+60h] [rbp-F8h] BYREF
  _QWORD v74[21]; // [rsp+68h] [rbp-F0h] BYREF
  __int64 v75[9]; // [rsp+110h] [rbp-48h] BYREF

  v70 = 0;
  *(_BYTE *)(a1 + 1736) = 0;
  if ( a4 != 0 )
    goto LABEL_2;
  sub_140F219E0(a1);
  v15 = *a2;
  v16 = *(_QWORD *)(a1 + 2000);
  if ( v16 != *a2 )
  {
    if ( v16 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v16)(a1: v16, a2: 1);
    *(_QWORD *)(a1 + 2000) = v15;
    if ( v15 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v15 + 8));
  }
  *(_BYTE *)(a1 + 1400) = a3;
  v75[0] = 0;
  sub_140F45A00(a1, a2: v74, a3, a4: v75);
  if ( v70 == v74[0] )
  {
    if ( v70 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v70 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v70)(a1: v70, a2: 1);
    v17 = v70;
  }
  else
  {
    if ( v70 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v70 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v70)(a1: v70, a2: 1);
    v17 = v74[0];
    v70 = v74[0];
  }
  LODWORD(v6) = 0;
  if ( v17 != 0 && (unsigned __int8)sub_140F4EEB0(a1, a2: &v70, a3, a4: 0) != 0 )
  {
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a2 + 120LL))(a1: *a2, a2: v74);
    if ( v74[0] == 0 )
    {
LABEL_211:
      *(_DWORD *)(a1 + 1520) = 0;
      if ( a5 != nullptr && a6 != nullptr )
        a6(a1: (unsigned int)*a5);
      v57 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
      if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
        (**v57)(a1: v57, a2: 1);
LABEL_2:
      if ( a5 != nullptr )
        ++*a5;
      v72 = a2;
      if ( a4 != 0 )
        goto LABEL_44;
      *(_BYTE *)(a1 + 1450) = 1;
      v11 = *(_QWORD *)(a1 + 8);
      v69 = nullptr;
      if ( (*(_BYTE *)(v11 + 92) & 2) != 0 )
      {
        *(_BYTE *)(v11 + 89) = 1;
        if ( a5 == nullptr )
          goto LABEL_44;
      }
      else
      {
        sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
        LODWORD(v6) = 0;
        sub_140FFADB0(a1: v11, a2: &v69, a3: 0, a4: 0);
        v74[0] = 0x80100004E554C4CLL;
        sub_1407D0F70(
          a1: (unsigned int)v74,
          a2: (unsigned int)&v71,
          a3: (unsigned int)&v70,
          a4: (unsigned int)&v69,
          a5: (__int64)v73,
          a6: 0,
          a7: 0,
          0);
        if ( v71 != 0 )
        {
          v74[0] = v71;
          _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
          LODWORD(v6) = sub_140F2BA20(a1: v11, a2: v74, a3: a1, a4: a3);
          v12 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
          if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
            (**v12)(a1: v12, a2: 1);
          v13 = (void (__fastcall ***)(_QWORD, __int64))v71;
          if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
            (**v13)(a1: v13, a2: 1);
        }
        v14 = v69;
        if ( v69 != nullptr && _InterlockedDecrement(v69 - 1) == 0 )
          sub_1412EC9A0(a1: v14 - 1);
        LODWORD(a2) = (_DWORD)v72;
        if ( (_BYTE)v6 == 0 )
          goto LABEL_275;
        if ( a5 == nullptr )
        {
LABEL_44:
          if ( (unsigned __int8)sub_1400870B0() != 0
            && (unsigned __int8)sub_1400015B0() == 0
            && *(_QWORD *)(*(_QWORD *)(qword_141B5FDB0 + 128) + 8LL) - **(_QWORD **)(qword_141B5FDB0 + 128) >= 0x3A981u
            && (_BYTE)a3 != 0 )
          {
            goto LABEL_275;
          }
          if ( a5 != nullptr )
            ++*a5;
          if ( a4 == 0 )
          {
            v20 = *(_QWORD *)(a1 + 16);
            v69 = nullptr;
            if ( (*(_BYTE *)(v20 + 92) & 2) != 0 )
            {
              *(_BYTE *)(v20 + 89) = 1;
            }
            else
            {
              sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
              LODWORD(v6) = 0;
              sub_140FFADB0(a1: v20, a2: &v69, a3: 0, a4: 0);
              v74[0] = 0x80100004E554C4CLL;
              LOBYTE(v68) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v74,
                a2: (unsigned int)&v71,
                a3: (unsigned int)&v70,
                a4: (unsigned int)&v69,
                a5: (__int64)v73,
                a6: 0,
                a7: 0,
                v68);
              if ( v71 != 0 )
              {
                v74[0] = v71;
                _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                LODWORD(v6) = sub_140F2BD50(a1: v20, a2: v74, a3: a1, a4: a3);
                v21 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                  (**v21)(a1: v21, a2: 1);
                v22 = (void (__fastcall ***)(_QWORD, __int64))v71;
                if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                  (**v22)(a1: v22, a2: 1);
              }
              v23 = v69;
              if ( v69 != nullptr && _InterlockedDecrement(v69 - 1) == 0 )
                sub_1412EC9A0(a1: v23 - 1);
              LODWORD(a2) = (_DWORD)v72;
              if ( (_BYTE)v6 == 0 )
                goto LABEL_275;
            }
            if ( a5 != nullptr && a6 != nullptr )
              a6(a1: (unsigned int)*a5);
          }
          if ( a5 != nullptr )
            ++*a5;
          if ( a4 == 0 )
          {
            v24 = *(_QWORD *)(a1 + 24);
            v69 = nullptr;
            if ( (*(_BYTE *)(v24 + 92) & 2) != 0 )
            {
              *(_BYTE *)(v24 + 89) = 1;
            }
            else
            {
              sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
              LODWORD(v6) = 0;
              sub_140FFADB0(a1: v24, a2: &v69, a3: 0, a4: 0);
              v74[0] = 0x80100004E554C4CLL;
              LOBYTE(v68) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v74,
                a2: (unsigned int)&v71,
                a3: (unsigned int)&v70,
                a4: (unsigned int)&v69,
                a5: (__int64)v73,
                a6: 0,
                a7: 0,
                v68);
              if ( v71 != 0 )
              {
                v74[0] = v71;
                _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                LODWORD(v6) = sub_140F2C060(a1: v24, a2: v74, a3: a1, a4: a3);
                v25 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                  (**v25)(a1: v25, a2: 1);
                v26 = (void (__fastcall ***)(_QWORD, __int64))v71;
                if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                  (**v26)(a1: v26, a2: 1);
              }
              v27 = v69;
              if ( v69 != nullptr && _InterlockedDecrement(v69 - 1) == 0 )
                sub_1412EC9A0(a1: v27 - 1);
              LODWORD(a2) = (_DWORD)v72;
              if ( (_BYTE)v6 == 0 )
                goto LABEL_275;
            }
            v32 = *(_QWORD *)(a1 + 32);
            v69 = nullptr;
            if ( (*(_BYTE *)(v32 + 92) & 2) != 0 )
            {
              *(_BYTE *)(v32 + 89) = 1;
            }
            else
            {
              sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
              LODWORD(v6) = 0;
              sub_140FFADB0(a1: v32, a2: &v69, a3: 0, a4: 0);
              v74[0] = 0x80100004E554C4CLL;
              LOBYTE(v68) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v74,
                a2: (unsigned int)&v71,
                a3: (unsigned int)&v70,
                a4: (unsigned int)&v69,
                a5: (__int64)v73,
                a6: 0,
                a7: 0,
                v68);
              if ( v71 != 0 )
              {
                v74[0] = v71;
                _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                LODWORD(v6) = sub_140F2C520(a1: v32, a2: v74, a3: a1, a4: a3);
                v33 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                  (**v33)(a1: v33, a2: 1);
                v34 = (void (__fastcall ***)(_QWORD, __int64))v71;
                if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                  (**v34)(a1: v34, a2: 1);
              }
              v35 = v69;
              if ( v69 != nullptr && _InterlockedDecrement(v69 - 1) == 0 )
                sub_1412EC9A0(a1: v35 - 1);
              LODWORD(a2) = (_DWORD)v72;
              if ( (_BYTE)v6 == 0 )
                goto LABEL_275;
            }
            v36 = *(_QWORD *)(a1 + 48);
            v69 = nullptr;
            if ( (*(_BYTE *)(v36 + 92) & 2) != 0 )
            {
              *(_BYTE *)(v36 + 89) = 1;
            }
            else
            {
              sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
              LODWORD(v6) = 0;
              sub_140FFADB0(a1: v36, a2: &v69, a3: 0, a4: 0);
              v74[0] = 0x80100004E554C4CLL;
              LOBYTE(v68) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v74,
                a2: (unsigned int)&v71,
                a3: (unsigned int)&v70,
                a4: (unsigned int)&v69,
                a5: (__int64)v73,
                a6: 0,
                a7: 0,
                v68);
              if ( v71 != 0 )
              {
                v74[0] = v71;
                _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                LODWORD(v6) = sub_140F2C9E0(a1: v36, a2: v74, a3: a1, a4: a3);
                v37 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                  (**v37)(a1: v37, a2: 1);
                v38 = (void (__fastcall ***)(_QWORD, __int64))v71;
                if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                  (**v38)(a1: v38, a2: 1);
              }
              v39 = v69;
              LODWORD(a2) = (_DWORD)v72;
              if ( v69 == nullptr || _InterlockedDecrement(v69 - 1) != 0 )
              {
                if ( (_BYTE)v6 == 0 )
                  goto LABEL_275;
              }
              else
              {
                sub_1412EC9A0(a1: v39 - 1);
                if ( (_BYTE)v6 == 0 )
                  goto LABEL_275;
              }
            }
            v44 = *(_QWORD *)(a1 + 80);
            v69 = nullptr;
            if ( (*(_BYTE *)(v44 + 92) & 2) != 0 )
            {
              *(_BYTE *)(v44 + 89) = 1;
            }
            else
            {
              sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
              LODWORD(v6) = 0;
              sub_140FFADB0(a1: v44, a2: &v69, a3: 0, a4: 0);
              v74[0] = 0x80100004E554C4CLL;
              LOBYTE(v68) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v74,
                a2: (unsigned int)&v71,
                a3: (unsigned int)&v70,
                a4: (unsigned int)&v69,
                a5: (__int64)v73,
                a6: 0,
                a7: 0,
                v68);
              if ( v71 != 0 )
              {
                v74[0] = v71;
                _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                LODWORD(v6) = sub_140F2D860(a1: v44, a2: v74, a3: a1, a4: a3);
                v45 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                  (**v45)(a1: v45, a2: 1);
                v46 = (void (__fastcall ***)(_QWORD, __int64))v71;
                if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                  (**v46)(a1: v46, a2: 1);
              }
              v47 = v69;
              LODWORD(a2) = (_DWORD)v72;
              if ( v69 == nullptr || _InterlockedDecrement(v69 - 1) != 0 )
              {
                if ( (_BYTE)v6 == 0 )
                  goto LABEL_275;
              }
              else
              {
                sub_1412EC9A0(a1: v47 - 1);
                if ( (_BYTE)v6 == 0 )
                  goto LABEL_275;
              }
            }
            if ( a5 != nullptr && a6 != nullptr )
              a6(a1: (unsigned int)*a5);
          }
          if ( a5 != nullptr )
            ++*a5;
          if ( a4 == 0 )
          {
            if ( *(unsigned __int16 *)(a1 + 1416) >= 0xDC4u )
            {
              v28 = *(_QWORD *)(a1 + 40);
              v69 = nullptr;
              if ( (*(_BYTE *)(v28 + 92) & 2) != 0 )
              {
                *(_BYTE *)(v28 + 89) = 1;
              }
              else
              {
                sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
                LODWORD(v6) = 0;
                sub_140FFADB0(a1: v28, a2: &v69, a3: 0, a4: 0);
                v74[0] = 0x80100004E554C4CLL;
                LOBYTE(v68) = 0;
                sub_1407D0F70(
                  a1: (unsigned int)v74,
                  a2: (unsigned int)&v71,
                  a3: (unsigned int)&v70,
                  a4: (unsigned int)&v69,
                  a5: (__int64)v73,
                  a6: 0,
                  a7: 0,
                  v68);
                if ( v71 != 0 )
                {
                  v74[0] = v71;
                  _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                  LODWORD(v6) = sub_140F2DD50(a1: v28, a2: v74, a3: a1, a4: a3);
                  v29 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                  if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                    (**v29)(a1: v29, a2: 1);
                  v30 = (void (__fastcall ***)(_QWORD, __int64))v71;
                  if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                    (**v30)(a1: v30, a2: 1);
                }
                v31 = v69;
                LODWORD(a2) = (_DWORD)v72;
                if ( v69 == nullptr || _InterlockedDecrement(v69 - 1) != 0 )
                {
                  if ( (_BYTE)v6 == 0 )
                    goto LABEL_275;
                }
                else
                {
                  sub_1412EC9A0(a1: v31 - 1);
                  if ( (_BYTE)v6 == 0 )
                    goto LABEL_275;
                }
              }
            }
            v58 = *(_QWORD *)(a1 + 96);
            v69 = nullptr;
            if ( (*(_BYTE *)(v58 + 92) & 2) != 0 )
            {
              *(_BYTE *)(v58 + 89) = 1;
            }
            else
            {
              sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
              LODWORD(v6) = 0;
              sub_140FFADB0(a1: v58, a2: &v69, a3: 0, a4: 0);
              v74[0] = 0x80100004E554C4CLL;
              LOBYTE(v68) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v74,
                a2: (unsigned int)&v71,
                a3: (unsigned int)&v70,
                a4: (unsigned int)&v69,
                a5: (__int64)v73,
                a6: 0,
                a7: 0,
                v68);
              if ( v71 != 0 )
              {
                v74[0] = v71;
                _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                LODWORD(v6) = sub_140F2E210(a1: v58, a2: v74, a3: a1, a4: a3);
                v59 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                  (**v59)(a1: v59, a2: 1);
                v60 = (void (__fastcall ***)(_QWORD, __int64))v71;
                if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                  (**v60)(a1: v60, a2: 1);
              }
              v61 = v69;
              if ( v69 != nullptr && _InterlockedDecrement(v69 - 1) == 0 )
                sub_1412EC9A0(a1: v61 - 1);
              LODWORD(a2) = (_DWORD)v72;
              if ( (_BYTE)v6 == 0 )
                goto LABEL_275;
            }
            if ( (unsigned __int8)sub_1410B9E50(a1: *(_QWORD *)(a1 + 200), a2: &v70) == 0
              || (unsigned __int8)sub_1410B9E50(a1: *(_QWORD *)(a1 + 208), a2: &v70) == 0
              || (unsigned __int8)sub_1410B9E50(a1: *(_QWORD *)(a1 + 216), a2: &v70) == 0
              || (unsigned __int8)sub_140F4F030(a1: *(_QWORD *)(a1 + 120), a2: &v70, a3: a1, a4: a3) == 0
              || (unsigned __int8)sub_140F4F160(a1: *(_QWORD *)(a1 + 88), a2: &v70, a3: a1, a4: a3) == 0 )
            {
              goto LABEL_275;
            }
            if ( a5 != nullptr && a6 != nullptr )
              a6(a1: (unsigned int)*a5);
          }
          if ( a5 != nullptr )
            ++*a5;
          if ( a4 == 0 )
          {
            v40 = *(_QWORD *)(a1 + 128);
            v69 = nullptr;
            if ( (*(_BYTE *)(v40 + 92) & 2) != 0 )
            {
              *(_BYTE *)(v40 + 89) = 1;
            }
            else
            {
              sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
              LODWORD(v6) = 0;
              sub_140FFADB0(a1: v40, a2: &v69, a3: 0, a4: 0);
              v74[0] = 0x80100004E554C4CLL;
              LOBYTE(v68) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v74,
                a2: (unsigned int)&v71,
                a3: (unsigned int)&v70,
                a4: (unsigned int)&v69,
                a5: (__int64)v73,
                a6: 0,
                a7: 0,
                v68);
              if ( v71 != 0 )
              {
                v74[0] = v71;
                _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                LODWORD(v6) = sub_140F2F1A0(a1: v40, a2: v74, a3: a1, a4: a3);
                v41 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                  (**v41)(a1: v41, a2: 1);
                v42 = (void (__fastcall ***)(_QWORD, __int64))v71;
                if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                  (**v42)(a1: v42, a2: 1);
              }
              v43 = v69;
              if ( v69 != nullptr && _InterlockedDecrement(v69 - 1) == 0 )
                sub_1412EC9A0(a1: v43 - 1);
              LODWORD(a2) = (_DWORD)v72;
              if ( (_BYTE)v6 == 0 )
                goto LABEL_275;
            }
            v48 = *(_QWORD *)(a1 + 136);
            v69 = nullptr;
            if ( (*(_BYTE *)(v48 + 92) & 2) != 0 )
            {
              *(_BYTE *)(v48 + 89) = 1;
            }
            else
            {
              sub_14080D0E0(a1: v73, a2: 0x1418E2C24LL);
              LODWORD(v6) = 0;
              sub_140FFADB0(a1: v48, a2: &v69, a3: 0, a4: 0);
              v74[0] = 0x80100004E554C4CLL;
              LOBYTE(v68) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v74,
                a2: (unsigned int)&v71,
                a3: (unsigned int)&v70,
                a4: (unsigned int)&v69,
                a5: (__int64)v73,
                a6: 0,
                a7: 0,
                v68);
              if ( v71 != 0 )
              {
                v74[0] = v71;
                _InterlockedIncrement((volatile signed __int32 *)(v71 + 8));
                LODWORD(v6) = sub_140F2F4B0(a1: v48, a2: v74, a3: a1, a4: a3);
                v49 = (void (__fastcall ***)(_QWORD, __int64))v74[0];
                if ( v74[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74[0] + 8LL)) == 0 )
                  (**v49)(a1: v49, a2: 1);
                v50 = (void (__fastcall ***)(_QWORD, __int64))v71;
                if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 + 8)) == 0 )
                  (**v50)(a1: v50, a2: 1);
              }
              v51 = v69;
              if ( v69 != nullptr && _InterlockedDecrement(v69 - 1) == 0 )
                sub_1412EC9A0(a1: v51 - 1);
              LODWORD(a2) = (_DWORD)v72;
              if ( (_BYTE)v6 == 0 )
                goto LABEL_275;
            }
            if ( (unsigned __int8)sub_140F4F290(a1: *(_QWORD *)(a1 + 184), a2: &v70, a3: a1, a4: a3) == 0
              || (unsigned __int8)sub_140F45C10(a1: *(_QWORD *)(a1 + 144), a2: &v70, a3: a1, a4: a3) == 0
              || (_BYTE)a3 != 0 && (unsigned __int8)sub_140F4F3C0(a1: *(_QWORD *)(a1 + 152), a2: &v70, a3: a1) == 0
              || (unsigned __int8)sub_140F4F4E0(a1: *(_QWORD *)(a1 + 160), a2: &v70, a3: a1, a4: a3) == 0 )
            {
              goto LABEL_275;
            }
            if ( a5 != nullptr && a6 != nullptr )
              a6(a1: (unsigned int)*a5);
          }
          if ( a5 != nullptr )
            ++*a5;
          if ( (_BYTE)a3 == 0 )
          {
LABEL_87:
            if ( a4 == 0 )
            {
              *(_BYTE *)(a1 + 1450) = 0;
              sub_140F3C890(a1, a2: 0);
              sub_140F4FE20(a1);
              LOBYTE(v67) = 0;
              sub_140F500A0(a1, (_DWORD)a2, a3: (unsigned int)&qword_141B5E470, a4: 0, a5: 0, a6: v67, a7: 0);
              sub_140F3F1A0(a1);
              sub_140F3F7E0(a1);
              sub_140F404F0(a1);
              sub_140F50DE0(a1: *(_QWORD *)(a1 + 944));
              sub_140F50E50(a1: *(_QWORD *)(a1 + 952));
              sub_14156F980();
              if ( a5 != nullptr && a6 != nullptr )
                a6(a1: (unsigned int)*a5);
            }
            if ( a5 != nullptr )
              ++*a5;
            LOBYTE(v6) = 1;
            if ( (_BYTE)a3 == 0 && a4 == 0 )
            {
              v74[0] = *(_QWORD *)(*(_QWORD *)(qword_141ABD468 + 8) + 64LL);
              sub_140F50EC0(a1, a2: (unsigned int)v74, a3: (_DWORD)a2, a4: 0, a5: 1, a6: 0, a7: 1, a8: 18);
              *(_WORD *)(a1 + 1416) = 3569;
            }
            goto LABEL_276;
          }
          if ( a4 != 0 )
          {
LABEL_82:
            if ( a5 != nullptr )
              ++*a5;
            if ( a4 == 0 )
            {
              if ( (unsigned __int8)sub_140F4FCD0(a1, a2: &v70) == 0 )
                goto LABEL_275;
              if ( a5 != nullptr && a6 != nullptr )
                a6(a1: (unsigned int)*a5);
              if ( (unsigned __int8)sub_141529AD0(a1: *(_QWORD *)(a1 + 1664), a2: &v70) == 0
                || (unsigned __int8)sub_14156F710(a1: *(_QWORD *)(a1 + 1672), a2: &v70) == 0
                || (unsigned __int8)sub_14156EBA0(a1: *(_QWORD *)(a1 + 1680), a2: &v70) == 0
                || (unsigned __int8)sub_14156F290(a1: *(_QWORD *)(a1 + 1688), a2: &v70) == 0 )
              {
                goto LABEL_275;
              }
            }
            if ( a5 != nullptr )
              ++*a5;
            goto LABEL_87;
          }
          if ( (unsigned __int8)sub_140F4F610(a1: *(_QWORD *)(a1 + 816), a2: &v70, a3: a1) != 0
            && (unsigned __int8)sub_140F4F730(a1: *(_QWORD *)(a1 + 848), a2: &v70, a3: a1) != 0
            && (unsigned __int8)sub_140F4F850(a1: *(_QWORD *)(a1 + 872), a2: &v70, a3: a1) != 0 )
          {
            v62 = *(unsigned __int16 *)(a1 + 1416);
            if ( v62 >= 0xDDD )
            {
              if ( (unsigned __int8)sub_1400015B0() == 0
                && ((unsigned __int8)sub_140F4F970(a1: *(_QWORD *)(a1 + 1032), a2: &v70, a3: a1) == 0
                 || (unsigned __int8)sub_140F4FA90(a1: *(_QWORD *)(a1 + 1024), a2: &v70, a3: a1) == 0) )
              {
                goto LABEL_275;
              }
              LOWORD(v62) = *(_WORD *)(a1 + 1416);
            }
            if ( (unsigned __int16)v62 > 0xDBFu
              || (sub_140F354B0(a1: v74),
                  v63 = sub_140F4FBB0(a1: v74, a2: &v70, a3: a1),
                  sub_140F35A80(a1: v74),
                  v64 = v63 == 0,
                  LODWORD(a2) = (_DWORD)v72,
                  !v64) )
            {
              if ( a5 != nullptr && a6 != nullptr )
                a6(a1: (unsigned int)*a5);
              goto LABEL_82;
            }
          }
LABEL_275:
          LODWORD(v6) = 0;
          goto LABEL_276;
        }
      }
      if ( a6 != nullptr )
        a6(a1: (unsigned int)*a5);
      goto LABEL_44;
    }
    (*(void (__fastcall **)(_QWORD, __int64 *))(*(_QWORD *)v74[0] + 16LL))(a1: v74[0], a2: &v71);
    v18 = (_DWORD *)v71;
    if ( v71 != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v71 - 4));
      v19 = v71;
      v69 = v18;
      if ( v71 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v71 - 4)) == 0 )
        sub_1412EC9A0(a1: v19 - 4);
    }
    else
    {
      v69 = nullptr;
    }
    v52 = *(int **)(a1 + 1424);
    v53 = (__int64)(v52 + 1);
    if ( v52 != nullptr )
    {
      v54 = *v52;
      v6 = v69;
      if ( v54 == -1 )
        goto LABEL_200;
      if ( v69 == nullptr )
      {
LABEL_199:
        if ( v54 == 0 )
        {
LABEL_200:
          v55 = (__int64)(v6 + 1);
          if ( v6 == nullptr )
            v55 = 0x1419435F1LL;
          if ( (unsigned int)sub_141758D90(a1: v55, a2: v53) == 0 )
            goto LABEL_208;
        }
LABEL_203:
        if ( (unsigned int)sub_141758D90(a1: v53, a2: 0x141938D12LL) == 0 )
        {
          v56 = (__int64)(v6 + 1);
          if ( v6 == nullptr )
            v56 = 0x1419435F1LL;
          if ( (unsigned int)sub_141758D90(a1: v56, a2: 0x1419387A7LL) == 0 )
          {
            sub_140809100(a1: a1 + 1424, a2: &v69);
            v6 = v69;
          }
        }
LABEL_208:
        if ( v6 != nullptr && _InterlockedDecrement(v6 - 1) == 0 )
          sub_1412EC9A0(a1: --v6);
        goto LABEL_211;
      }
    }
    else
    {
      v53 = 0x1419435F1LL;
      v54 = 0;
      v6 = v69;
      if ( v69 == nullptr )
        goto LABEL_199;
    }
    if ( *v6 == v54 )
      goto LABEL_200;
    goto LABEL_203;
  }
LABEL_276:
  v65 = (void (__fastcall ***)(_QWORD, __int64))v70;
  if ( v70 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v70 + 8)) == 0 )
    (**v65)(a1: v65, a2: 1);
  return (unsigned int)v6;
}
