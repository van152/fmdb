__int64 __fastcall sub_140049BB0(__int64 a1, char a2)
{
  __int64 *v2; // rsi
  __int64 v4; // rdi
  char v5; // bl
  int v6; // r8d
  _QWORD *v7; // r14
  __int64 v8; // r12
  __int64 v9; // r13
  __int64 v10; // r8
  __int64 v11; // r9
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  __int64 v13; // rax
  unsigned __int64 v14; // rbp
  __int64 v15; // rbx
  unsigned __int64 v16; // rsi
  __int64 v17; // r13
  unsigned __int64 v18; // rbp
  int v19; // eax
  __int64 v20; // rax
  _QWORD *v21; // rdi
  _QWORD *i; // r12
  __int64 v23; // r15
  __int64 v24; // rax
  __int64 v25; // rsi
  __int64 v26; // rax
  __int64 v27; // rax
  __int64 v28; // rdx
  char v29; // cl
  unsigned __int64 v30; // rbp
  __int64 v31; // r15
  __int64 v32; // rsi
  void (__fastcall ***v33)(_QWORD, __int64); // rcx
  _QWORD *v34; // rax
  __int64 v35; // rsi
  int v36; // edi
  int v37; // eax
  int v38; // r8d
  __int64 v39; // rdx
  _QWORD *v40; // rax
  void (__fastcall ***v41)(_QWORD, __int64); // rcx
  void (__fastcall ***v42)(_QWORD, __int64); // rcx
  char v44; // [rsp+67h] [rbp-101h] BYREF
  __int64 v45; // [rsp+68h] [rbp-100h] BYREF
  _QWORD v46[2]; // [rsp+70h] [rbp-F8h] BYREF
  __int64 v47; // [rsp+80h] [rbp-E8h] BYREF
  __int64 v48; // [rsp+88h] [rbp-E0h]
  __int64 v49; // [rsp+90h] [rbp-D8h]
  __int64 v50; // [rsp+98h] [rbp-D0h]
  unsigned __int64 v51; // [rsp+A0h] [rbp-C8h]
  __int64 v52; // [rsp+A8h] [rbp-C0h] BYREF
  __int64 v53; // [rsp+B0h] [rbp-B8h]
  __int64 v54; // [rsp+B8h] [rbp-B0h]
  __int64 v55; // [rsp+C8h] [rbp-A0h]
  _QWORD v56[2]; // [rsp+D8h] [rbp-90h] BYREF
  __int64 v57; // [rsp+E8h] [rbp-80h]
  _QWORD v58[2]; // [rsp+F8h] [rbp-70h] BYREF
  __int64 v59; // [rsp+108h] [rbp-60h]

  LOBYTE(v2) = 1;
  if ( a2 != 0 )
    return (unsigned int)v2;
  BYTE4(qword_141B5E498) &= ~1u;
  v4 = qword_141ABDFE8;
  LODWORD(v2) = 0;
  sub_14083D6D0(a1: &v52, a2: 0);
  v5 = sub_140800A10(a1: v4, a2: &unk_141ABFC88, a3: &v52, a4: 0);
  sub_14083D320(a1: &v52);
  LOBYTE(v6) = 1;
  if ( (unsigned __int8)sub_14000F400(
                          a1,
                          a2: 0,
                          a3: v6,
                          a4: 0,
                          a5: 0,
                          a6: 0,
                          a7: 1,
                          a8: (__int64)&qword_141B59EE0,
                          a9: (__int64)&qword_141B59EE0,
                          a10: 1,
                          a11: v5,
                          a12: 1) == 0 )
    return (unsigned int)v2;
  LOBYTE(word_141B60460) = 3;
  sub_1407D5DC0(a1: qword_141ABD878, a2: &v47, a3: &qword_141B5EDF0);
  sub_140F5AA50(a1: &qword_141B5FDA8, a2: 0);
  v7 = (_QWORD *)qword_141ABD830;
  *(_WORD *)(qword_141ABD830 + 1347) = 257;
  v8 = v7[3];
  v9 = v7[4];
  if ( v9 != v8 )
    goto LABEL_49;
  v48 = v7[4];
  v49 = v8;
  v50 = a1;
  v52 = 0;
  nullsub_1(a1: v7 + 1, a2: &v52);
  v12 = (void (__fastcall ***)(_QWORD, __int64))v52;
  if ( v52 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v52 + 8)) == 0 )
    (**v12)(a1: v12, a2: 1);
  v13 = *(_QWORD *)(qword_141ABF5C0 + 44424);
  if ( *(_QWORD *)(qword_141ABF5C0 + 44432) != v13 )
  {
    v14 = 0;
    do
    {
      v15 = sub_14083E160(a1: *(_QWORD *)(v13 + 8 * v14));
      v52 = 0x14175CD28LL;
      v53 = v15;
      LOBYTE(v54) = 1;
      if ( (unsigned __int8)sub_140CD9140(a1: &v52, a2: v46) == 0 || LOBYTE(v46[0]) == 0 )
      {
        sub_140833AD0(a1: &v52, a2: v15);
        sub_1408916D0(
          a1: qword_141B5AD60,
          a2: (unsigned int)&v52,
          a3: 0,
          a4: 0,
          a5: (__int64)&qword_141B5A4A0,
          a6: (__int64)&qword_141B5A458,
          a7: 0,
          a8: 0);
        sub_140833970(a1: &v52);
      }
      ++v14;
      v13 = *(_QWORD *)(qword_141ABF5C0 + 44424);
    }
    while ( v14 < (*(_QWORD *)(qword_141ABF5C0 + 44432) - v13) >> 3 );
  }
  LOBYTE(v10) = 1;
  LOBYTE(v11) = 1;
  (*(void (__fastcall **)(__int64, _QWORD, __int64, __int64))(*(_QWORD *)qword_141B5AD60 + 600LL))(
    a1: qword_141B5AD60,
    a2: 0,
    a3: v10,
    a4: v11);
  if ( sub_140F459E0() != 0 )
  {
    v16 = 0;
    do
    {
      v51 = v16;
      v17 = sub_140F45D40(a1: (unsigned int)v16);
      if ( sub_140EBF5F0(a1: v17) != 0 )
      {
        v18 = 0;
        do
        {
          v19 = sub_140EBF480(a1: v17, a2: v18);
          sub_140A2DC30(a1: (unsigned int)&v52, a2: v19, a3: v17, a4: 0, a5: 0);
          v20 = sub_140835850(a1: v53, a2: 1668441972);
          v21 = (_QWORD *)sub_14083E140(a1: v20);
          for ( i = (_QWORD *)*v21; i != (_QWORD *)v21[1]; ++i )
          {
            v23 = sub_14083E160(a1: *i);
            if ( (unsigned __int8)sub_1408357E0(a1: v23, a2: 1416914273) != 0 )
            {
              v46[0] = 0;
              v24 = sub_140835850(a1: v23, a2: 1416914273);
              sub_140FE7E20(a1: v46, a2: v24);
              if ( v46[0] != 0 && ((__int64 (*)(void))sub_1411C2B70)() != 0 )
              {
                v25 = v7[10];
                v26 = sub_1411C2B70(a1: v46[0]);
                sub_140CB3970(a1: v25, a2: *(unsigned int *)(v26 + 12));
              }
            }
          }
          ++v18;
        }
        while ( v18 < sub_140EBF5F0(a1: v17) );
      }
      v16 = v51 + 1;
    }
    while ( v16 < sub_140F459E0() );
  }
  sub_14083D2C0(a1: v46);
  if ( (unsigned __int8)sub_140800D80(a1: qword_141ABDFE8, a2: &unk_141ABFCB0, a3: v46) != 0 )
  {
    v27 = qword_141B5AD60;
    v28 = *(_QWORD *)(qword_141B5AD60 + 16);
    if ( *(_QWORD *)(qword_141B5AD60 + 24) != v28 )
    {
      v29 = 1;
      v30 = 0;
      do
      {
        v31 = *(_QWORD *)(v28 + 8 * v30);
        if ( *(_BYTE *)(v31 + 73) != 0 )
        {
          v32 = qword_141ABD468;
          v45 = 0;
          sub_140809040(a1: &v45, a2: 0x14191A400LL, a3: 0xFFFFFFFFLL);
          sub_140824A20(a1: v32, a2: &v52, a3: &v45);
          sub_140808B00(a1: &v45);
          sub_140FE3E30(a1: &v45, a2: *(_QWORD *)(v31 + 24));
          sub_14081D7C0(a1: &v52, a2: 1, a3: &v45, a4: 0);
          v33 = (void (__fastcall ***)(_QWORD, __int64))v45;
          if ( v45 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v45 + 8)) == 0 )
            (**v33)(a1: v33, a2: 1);
          if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
          {
            v34 = &unk_141ABD978;
            while ( 1 )
            {
              v34 = (_QWORD *)v34[2];
              if ( v34 == nullptr || *v34 == 0 )
                break;
              if ( (*((_BYTE *)v34 + 28) & 1) == 0 || *((int *)v34 + 6) > 1 )
                goto LABEL_30;
            }
            v35 = sub_1407E2C90(a1: 2160);
            sub_1407E2EB0(a1: v35, a2: 1099914335, a3: 19412, a4: 1099882418, a5: 0, a6: 1);
            sub_14081ED40(a1: &v52, a2: &v45, a3: 0);
            sub_1407D6070(a1: v35, a2: &v45);
            sub_140808B00(a1: &v45);
            if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v35) & 4) != 0 )
              sub_1407CD750();
          }
LABEL_30:
          sub_14081D040(a1: &v52);
          v29 = 0;
          v27 = qword_141B5AD60;
        }
        ++v30;
        v28 = *(_QWORD *)(v27 + 16);
      }
      while ( v30 < (*(_QWORD *)(v27 + 24) - v28) >> 3 );
      if ( (v29 & 1) == 0 )
      {
        sub_14083D320(a1: v46);
        LODWORD(v2) = 0;
LABEL_74:
        v42 = (void (__fastcall ***)(_QWORD, __int64))v47;
        if ( v47 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v47 + 8)) == 0 )
          (**v42)(a1: v42, a2: 1);
        return (unsigned int)v2;
      }
    }
  }
  sub_14083D320(a1: v46);
  a1 = v50;
  v8 = v49;
  v9 = v48;
LABEL_49:
  v36 = qword_141B5AD60;
  *(_BYTE *)(qword_141B5AD60 + 1339) = 1;
  v52 = 0;
  v2 = &v52;
  sub_140809040(a1: &v52, a2: 0x14192DD12LL, a3: 0xFFFFFFFFLL);
  sub_1408B1260(
    a1: v36,
    a2: (unsigned int)&v52,
    a3: (unsigned int)&qword_141B59EE0,
    a4: (unsigned int)&qword_141B59EE0,
    a5: (__int64)v46,
    a6: -1,
    a7: 0,
    a8: 0,
    a9: 0,
    a10: 0,
    a11: 0);
  sub_140808B00(a1: &v52);
  v45 = 0;
  sub_140F5B9D0(a1: (unsigned int)&v52, a2: (unsigned __int8)byte_141B60462, a3: 0, a4: 0, a5: 0);
  v37 = sub_1404377F0(a1: &qword_141B5FDA8);
  sub_140F5C8A0(
    a1: (unsigned int)&qword_141B5FDA8,
    a2: v37,
    a3: 0,
    a4: 0,
    a5: 0,
    a6: (__int64)&v52,
    a7: (__int64)&v45,
    a8: (__int64)&v45,
    a9: 0,
    a10: 300);
  sub_140F75CF0(a1: &qword_141B5FDA8);
  sub_140F75D70(a1: &qword_141B5FDA8);
  sub_14011BE90(a1: qword_141ABF5C0, a2: 0, a3: 30, a4: 0, a5: (__int64)&qword_141B59EE0, a6: 0);
  sub_140F62A50(a1: 0);
  if ( (unsigned __int8)sub_140F62A70() == 0 )
  {
    v2 = &qword_141B5FDA8;
    do
    {
      v44 = 0;
      LOBYTE(v38) = 1;
      sub_140F64530(
        a1: (unsigned int)&qword_141B5FDA8,
        a2: (unsigned int)&v47,
        a3: v38,
        a4: (unsigned int)&v44,
        a5: 1,
        a6: (__int64)sub_14011C380,
        a7: 0);
    }
    while ( (unsigned __int8)sub_140F62A70() == 0 );
  }
  sub_14011C160(a1: qword_141ABF5C0);
  sub_140F76C90(a1: &qword_141B5FDA8, a2: 0);
  sub_14004A4D0();
  sub_14004AD20();
  if ( v9 == v8 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 760LL))(a1: qword_141B5AD60);
  LOBYTE(v39) = 3;
  sub_140048920(a1, a2: v39, a3: 0, a4: 0);
  if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
  {
    v40 = &unk_141ABD978;
    while ( 1 )
    {
      v40 = (_QWORD *)v40[2];
      if ( v40 == nullptr || *v40 == 0 )
        break;
      if ( (*((_BYTE *)v40 + 28) & 1) == 0 || *((int *)v40 + 6) > 1 )
        goto LABEL_64;
    }
    v2 = (__int64 *)sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: (_DWORD)v2, a2: 1099914335, a3: 19465, a4: 1099882418, a5: 0, a6: 1);
    sub_1407E0010(a1: v2, a2: 0x1418EC705LL);
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v2) & 4) != 0 )
      sub_1407CD750();
  }
LABEL_64:
  LOBYTE(word_141B60460) = 6;
  if ( v58[0] != 0 )
  {
    v2 = v58;
    sub_1407E4890(a1: qword_141ABD470, a2: v58[0], a3: v59 - v58[0]);
    v59 = 0;
    v58[1] = 0;
    v58[0] = 0;
  }
  if ( v56[0] != 0 )
  {
    v2 = v56;
    sub_1407E4890(a1: qword_141ABD470, a2: v56[0], a3: v57 - v56[0]);
    v57 = 0;
    v56[1] = 0;
    v56[0] = 0;
  }
  if ( v54 != 0 )
    sub_1407E4890(a1: qword_141ABD470, a2: v54, a3: v55 - v54);
  v41 = (void (__fastcall ***)(_QWORD, __int64))v45;
  if ( v45 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v45 + 16)) == 0 )
    (**v41)(a1: v41, a2: 1);
  LOBYTE(v2) = 1;
  goto LABEL_74;
}
