__int64 __fastcall sub_1400959F0(__int64 a1, _QWORD *a2, __int64 a3, __int64 a4)
{
  _QWORD *v6; // r14
  __int64 v8; // rdi
  __int64 v9; // rax
  unsigned int v10; // ebx
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  char v12; // r15
  _QWORD *v13; // rbx
  __int64 v14; // rdx
  __int64 v15; // rcx
  char v16; // di
  int v17; // r8d
  int v18; // r9d
  int v19; // r9d
  int v20; // eax
  _QWORD *v21; // rax
  __int64 v22; // rdx
  __int64 v23; // rcx
  char v24; // al
  unsigned __int64 v25; // rax
  _QWORD *v26; // rax
  __int64 v27; // rsi
  __int64 v28; // rdx
  __int64 v29; // rdi
  __int64 v30; // rax
  __int64 v31; // r9
  __int64 v32; // rdi
  __int64 v33; // rax
  __int64 v34; // r9
  volatile signed __int32 *v35; // rsi
  unsigned __int64 v36; // rbp
  volatile signed __int32 *v37; // rbx
  void (__fastcall ***v38)(_QWORD, __int64); // rcx
  volatile signed __int32 *v39; // rcx
  __int64 v40; // rax
  __int64 v41; // rax
  void (__fastcall ***v42)(_QWORD, __int64); // rcx
  volatile signed __int32 *v43; // rsi
  void (__fastcall ***v44)(_QWORD, __int64); // rcx
  volatile signed __int32 *v45; // rcx
  __int64 v46; // rcx
  char v48; // [rsp+4Fh] [rbp-B9h]
  volatile signed __int32 *v49; // [rsp+50h] [rbp-B8h] BYREF
  volatile signed __int32 *v50; // [rsp+58h] [rbp-B0h] BYREF
  _QWORD v51[2]; // [rsp+60h] [rbp-A8h] BYREF
  int v52; // [rsp+74h] [rbp-94h]
  _QWORD *v53; // [rsp+78h] [rbp-90h]
  volatile signed __int32 *v54[3]; // [rsp+80h] [rbp-88h] BYREF
  __int64 v55; // [rsp+98h] [rbp-70h]
  __int16 v56; // [rsp+A0h] [rbp-68h] BYREF
  __int64 v57; // [rsp+A8h] [rbp-60h] BYREF
  __int64 v58; // [rsp+B0h] [rbp-58h] BYREF
  _BYTE v59[4]; // [rsp+B8h] [rbp-50h] BYREF
  unsigned __int16 v60; // [rsp+BCh] [rbp-4Ch]
  _BYTE v61[72]; // [rsp+C0h] [rbp-48h] BYREF

  if ( *a2 == 0 )
    return 0;
  v6 = a2;
  sub_140AFEBC0(a1: qword_141ABF5C0 + 448);
  v49 = nullptr;
  sub_1407D0D60(a1: v59);
  sub_1407D0F70(a1: (unsigned int)v59, a2: (unsigned int)&v57, a3: (_DWORD)v6, a4: a3, a5: a4, a6: 0, a7: 0, a8: 0);
  if ( v60 <= 1u )
  {
    if ( qword_141ABF5C0 != 0 && *(_QWORD *)(qword_141ABF5C0 + 296) != 0 )
    {
      sub_1407C9510(a1: v54);
      sub_14083D9C0(a1: v51, a2: 0x1418DD191LL);
      sub_140835380(a1: v54, a2: 1953068140, a3: v51);
      sub_14083D320(a1: v51);
      sub_14083D9C0(a1: v51, a2: 0x14190CA84LL);
      sub_140835380(a1: v54, a2: 1952807028, a3: v51);
      sub_14083D320(a1: v51);
      v8 = sub_140199090(a1: qword_141ABDFF8);
      v9 = sub_140199090(a1: qword_141ABDFF8);
      v10 = 0;
      sub_140170850(a1: v9, a2: v8, a3: v54, a4: 0);
      sub_140833970(a1: v54);
      goto LABEL_87;
    }
    v10 = 0;
    if ( (dword_141ABD994 & 1) == 0 || dword_141ABD990 > 1 )
      goto LABEL_87;
    v21 = &unk_141ABD978;
    while ( 1 )
    {
      v21 = (_QWORD *)v21[2];
      if ( v21 == nullptr || *v21 == 0 )
        break;
      if ( (*((_BYTE *)v21 + 28) & 1) == 0 || *((int *)v21 + 6) > 1 )
        goto LABEL_86;
    }
    v27 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v27, a2: 1099915787, a3: 1450, a4: 1099812390, a5: 0, a6: 1);
    v28 = 0x141909654LL;
    goto LABEL_84;
  }
  if ( v57 != 0 )
  {
    v51[0] = v57;
    _InterlockedIncrement((volatile signed __int32 *)(v57 + 8));
    sub_1407C5A20(a1: v54, a2: v51, a3: v6, a4: a3);
    if ( v49 != v54[0] )
    {
      v49 = v54[0];
      v54[0] = nullptr;
    }
    v11 = (void (__fastcall ***)(_QWORD, __int64))v51[0];
    if ( v51[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v51[0] + 8LL)) == 0 )
      (**v11)(a1: v11, a2: 1);
  }
  if ( v49 == nullptr )
  {
    if ( qword_141ABF5C0 == 0 || *(_QWORD *)(qword_141ABF5C0 + 296) == 0 )
    {
      v10 = 0;
      if ( (dword_141ABD994 & 1) == 0 || dword_141ABD990 > 1 )
        goto LABEL_87;
      v26 = &unk_141ABD978;
      v10 = 0;
      while ( 1 )
      {
        v26 = (_QWORD *)v26[2];
        if ( v26 == nullptr || *v26 == 0 )
          break;
        if ( (*((_BYTE *)v26 + 28) & 1) == 0 )
          goto LABEL_86;
        if ( *((int *)v26 + 6) > 1 )
          goto LABEL_87;
      }
      v27 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v27, a2: 1099915787, a3: 1471, a4: 1099812390, a5: 0, a6: 1);
      v28 = 0x1418DCE8CLL;
      goto LABEL_84;
    }
    sub_1407C9510(a1: v54);
    sub_14083D9C0(a1: v51, a2: 0x1418DD191LL);
    sub_140835380(a1: v54, a2: 1953068140, a3: v51);
    sub_14083D320(a1: v51);
    v22 = 0x1418DCE8CLL;
LABEL_46:
    sub_14083D9C0(a1: v51, a2: v22);
    sub_140835380(a1: v54, a2: 1952807028, a3: v51);
    sub_14083D320(a1: v51);
    v29 = sub_140199090(a1: qword_141ABDFF8);
    v30 = sub_140199090(a1: qword_141ABDFF8);
    LOBYTE(v31) = 1;
    sub_140170850(a1: v30, a2: v29, a3: v54, a4: v31);
    sub_140833970(a1: v54);
    goto LABEL_86;
  }
  sub_140AFEAF0(a1: qword_141ABF5C0 + 448, a2: 0);
  sub_1407D8AB0(a1: v54, a2: 0x1418E2C24LL);
  v50 = nullptr;
  sub_140809040(a1: &v50, a2: 0x141923096LL, a3: 0xFFFFFFFFLL);
  sub_1407D5F40(a1: v51, a2: &v50);
  v12 = (*(__int64 (__fastcall **)(volatile signed __int32 *, _QWORD *, volatile signed __int32 **))(*(_QWORD *)v49 + 192LL))(
          a1: v49,
          a2: v51,
          a3: v54);
  sub_140808B00(a1: v51);
  sub_140808B00(a1: &v50);
  *(_BYTE *)(a1 + 1372) = v12 ^ 1;
  sub_1400937A0(a1: a1 + 8);
  *(_BYTE *)(qword_141ABF5C0 + 44649) = 0;
  if ( v12 != 1 )
  {
    if ( (unsigned __int8)sub_140F6F400() != 0 )
    {
      v24 = sub_140096810(a1: v23, a2: &v49);
      v53 = v6;
      v48 = v12;
      v55 = a1 + 8;
      if ( v24 != 0 )
      {
        v25 = sub_14000FDF0(a1: (_QWORD *)qword_141ABF5C0);
        LOBYTE(v25) = 1;
        v52 = v25;
      }
      else
      {
        v52 = 0;
      }
LABEL_53:
      v54[0] = nullptr;
      v35 = v49;
      sub_1407D8AB0(a1: v51, a2: 0x1418DF862LL);
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64 *, _QWORD *, volatile signed __int32 **, int))(*(_QWORD *)v35 + 216LL))(
        a1: v35,
        a2: &v50,
        a3: &qword_141B59758,
        a4: v51,
        a5: v54,
        a6: 4);
      sub_1407D5DC0(a1: qword_141ABD878, a2: v51, a3: &qword_141B59838);
      if ( v51[0] != 0 && v54[0] != nullptr && sub_1404B4FD0(a1: v54[0]) != 0 )
      {
        v36 = 0;
        do
        {
          sub_1407D4680(a1: v54[0], a2: &v50, a3: v36);
          v37 = v50;
          (*(void (__fastcall **)(volatile signed __int32 *, __int16 *))(*(_QWORD *)v50 + 24LL))(a1: v50, a2: &v56);
          (*(void (__fastcall **)(volatile signed __int32 *, _BYTE *))(*(_QWORD *)v50 + 16LL))(a1: v50, a2: v61);
          (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, _BYTE *, __int16 *, _QWORD *, _DWORD))(*(_QWORD *)v37 + 144LL))(
            a1: v37,
            a2: &v58,
            a3: v61,
            a4: &v56,
            a5: v51,
            a6: 0);
          v38 = (void (__fastcall ***)(_QWORD, __int64))v58;
          if ( v58 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v58 + 8)) == 0 )
            (**v38)(a1: v38, a2: 1);
          sub_140808B00(a1: v61);
          v39 = v50;
          if ( v50 != nullptr && _InterlockedDecrement(v50 + 2) == 0 )
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v39)(a1: v39, a2: 1);
          ++v36;
        }
        while ( v36 < sub_1404B4FD0(a1: v54[0]) );
      }
      if ( (_BYTE)v52 != 0
        && (unsigned __int8)sub_1408A58A0(a1: v55, a2: &v49) != 0
        && (v40 = sub_140096AE0(), (unsigned __int8)sub_141204E80(a1: v40, a2: &v49) != 0) )
      {
        v10 = sub_140096B90(a1, a2: &v49);
        sub_14011C160(a1: qword_141ABF5C0);
        if ( (_BYTE)v10 != 0 )
        {
          *(_DWORD *)(a1 + 1272) = dword_141AAE084;
          v6 = v53;
          if ( *(_BYTE *)(a1 + 1352) == 0 )
            *(_BYTE *)(a1 + 1369) = v48;
          v41 = sub_1400015F0(a1: a3);
          sub_140809100(a1: a1 + 1520, a2: v41);
          LOBYTE(v10) = 1;
          goto LABEL_73;
        }
      }
      else
      {
        sub_14011C160(a1: qword_141ABF5C0);
      }
      v10 = 0;
      v6 = v53;
LABEL_73:
      if ( *(_BYTE *)(a1 + 1374) == 0 )
        *(_BYTE *)(a1 + 1528) = 1;
      v42 = (void (__fastcall ***)(_QWORD, __int64))v51[0];
      if ( v51[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v51[0] + 8LL)) == 0 )
        (**v42)(a1: v42, a2: 1);
      v43 = v54[0];
      if ( v54[0] != nullptr && _InterlockedDecrement(v54[0]) == 0 )
      {
        sub_1400532D0(a1: v43);
        sub_141750CFC(a1: v43);
      }
      goto LABEL_87;
    }
    if ( qword_141ABF5C0 == 0 || *(_QWORD *)(qword_141ABF5C0 + 296) == 0 )
    {
      if ( (unsigned __int8)sub_14000F6A0(a1: &unk_141ABD978, a2: 1) == 0 )
        goto LABEL_86;
      v27 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v27, a2: 1099915787, a3: 1532, a4: 1099812390, a5: 0, a6: 1);
      v28 = 0x14191B08ALL;
      goto LABEL_84;
    }
    sub_1407C9510(a1: v54);
    sub_14083D9C0(a1: v51, a2: 0x1418DD191LL);
    sub_140835380(a1: v54, a2: 1953068140, a3: v51);
    sub_14083D320(a1: v51);
    v22 = 0x14191B01CLL;
    goto LABEL_46;
  }
  v55 = a1 + 8;
  v13 = *(_QWORD **)(a1 + 1408);
  sub_1400D9400(a1: a1 + 1408, a2: a1 + 1408, a3: v13[1]);
  v13[1] = v13;
  *v13 = v13;
  v13[2] = v13;
  *(_QWORD *)(a1 + 1416) = 0;
  *(_DWORD *)(a1 + 1392) = 0;
  nullsub_1(a1: v15, a2: v14);
  v16 = sub_140096580(a1, a2: &v49);
  LOWORD(v50) = 30;
  LOBYTE(v17) = 1;
  LOBYTE(v18) = 1;
  if ( (unsigned __int8)sub_140F29230(
                          a1: (unsigned int)&qword_141B5FDA8,
                          a2: (unsigned int)&v49,
                          a3: v17,
                          a4: v18,
                          a5: (__int64)&v50,
                          a6: 0) != 0 )
  {
    sub_14011BE90(a1: qword_141ABF5C0, a2: 0, a3: (__int16)v50, a4: 0, a5: (__int64)&qword_141B59EE0, a6: 0);
    v56 = 0;
    if ( v16 != 0 )
    {
      LOBYTE(v19) = 1;
      v20 = sub_140F29230(
              a1: (unsigned int)&qword_141B5FDA8,
              a2: (unsigned int)&v49,
              a3: 0,
              a4: v19,
              a5: (__int64)&v56,
              a6: (__int64)sub_14011C380);
      if ( (_BYTE)v20 != 0 )
      {
        LOBYTE(v20) = 1;
        v52 = v20;
        v48 = v12;
        v53 = v6;
        goto LABEL_53;
      }
    }
    if ( qword_141ABF5C0 != 0 && *(_QWORD *)(qword_141ABF5C0 + 296) != 0 )
    {
      sub_1407C9510(a1: v54);
      sub_14083D9C0(a1: v51, a2: 0x1418DD191LL);
      sub_140835380(a1: v54, a2: 1953068140, a3: v51);
      sub_14083D320(a1: v51);
      sub_14083D9C0(a1: v51, a2: 0x14190BF95LL);
      sub_140835380(a1: v54, a2: 1952807028, a3: v51);
      sub_14083D320(a1: v51);
      v32 = sub_140199090(a1: qword_141ABDFF8);
      v33 = sub_140199090(a1: qword_141ABDFF8);
      LOBYTE(v34) = 1;
      sub_140170850(a1: v33, a2: v32, a3: v54, a4: v34);
      sub_14011C160(a1: qword_141ABF5C0);
      sub_140833970(a1: v54);
      goto LABEL_86;
    }
    sub_140F219E0(a1: &qword_141B5FDA8);
    if ( (unsigned __int8)sub_14000F6A0(a1: &unk_141ABD978, a2: 1) == 0 )
      goto LABEL_86;
    v27 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v27, a2: 1099915787, a3: 1514, a4: 1099812390, a5: 0, a6: 1);
    v28 = 0x14190BF95LL;
LABEL_84:
    sub_1407E0010(a1: v27, a2: v28);
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v27) & 4) != 0 )
      sub_1407CD750();
  }
LABEL_86:
  v10 = 0;
LABEL_87:
  v44 = (void (__fastcall ***)(_QWORD, __int64))v57;
  if ( v57 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v57 + 8)) == 0 )
    (**v44)(a1: v44, a2: 1);
  v45 = v49;
  if ( v49 != nullptr && _InterlockedDecrement(v49 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v45)(a1: v45, a2: 1);
  v46 = *v6;
  if ( *v6 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v46 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v46)(a1: v46, a2: 1);
  return v10;
}
