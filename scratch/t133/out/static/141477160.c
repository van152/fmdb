__int64 __fastcall sub_141477160(__int64 a1, volatile signed __int32 **a2, __int64 a3, __int64 a4)
{
  volatile signed __int32 *v5; // rax
  char *v6; // rdi
  __int64 v7; // rax
  __int64 v8; // rsi
  char *v9; // r13
  __int64 v10; // rdi
  __int64 v11; // rax
  char *v12; // r15
  __int64 v13; // r8
  bool v14; // zf
  volatile signed __int32 *v15; // rbx
  __int64 v16; // rax
  __int64 v17; // rax
  __int64 v18; // rdi
  char *v19; // r15
  char v20; // al
  char *v21; // rsi
  __int64 v22; // r8
  __int64 v23; // rax
  __int64 v24; // rsi
  char v25; // r14
  __int64 v26; // rsi
  unsigned __int8 *v27; // rdi
  unsigned __int64 v28; // rax
  __int64 v29; // r15
  unsigned __int8 v30; // al
  unsigned int v31; // esi
  volatile signed __int32 *v32; // rcx
  char *v34; // rbx
  char *v35; // r14
  char *v36; // rsi
  char *v37; // rdi
  __int64 v38; // r8
  volatile signed __int32 *v39; // rcx
  char *v40; // rdi
  char *v41; // r14
  char *v42; // rdi
  char *v43; // rsi
  __int64 v44; // r8
  char v45; // di
  __int64 v46; // rsi
  char *v47; // rdi
  char *v48; // r13
  char *v49; // rbx
  char *v50; // rsi
  __int64 v51; // r8
  __int64 v52; // r8
  unsigned int v53; // eax
  char *v56; // [rsp+68h] [rbp-18h]
  char *v57; // [rsp+70h] [rbp-10h]
  __int64 v58; // [rsp+78h] [rbp-8h]
  char *v59; // [rsp+88h] [rbp+8h]
  char *v60; // [rsp+90h] [rbp+10h]
  __int64 v61; // [rsp+98h] [rbp+18h] BYREF
  __int64 v62; // [rsp+A0h] [rbp+20h]
  __int64 v63; // [rsp+A8h] [rbp+28h]
  char *v64; // [rsp+B0h] [rbp+30h]
  char *v65; // [rsp+B8h] [rbp+38h]
  char *v66; // [rsp+C0h] [rbp+40h]
  char *v67; // [rsp+C8h] [rbp+48h]
  char *v68; // [rsp+D0h] [rbp+50h]
  char *v69; // [rsp+D8h] [rbp+58h]
  char *v70; // [rsp+E0h] [rbp+60h]
  volatile signed __int32 *v71; // [rsp+E8h] [rbp+68h] BYREF
  char *v72; // [rsp+F0h] [rbp+70h]
  __int64 v73; // [rsp+F8h] [rbp+78h]
  char *v74; // [rsp+100h] [rbp+80h]
  char v75; // [rsp+10Fh] [rbp+8Fh] BYREF
  _QWORD v76[8]; // [rsp+110h] [rbp+90h] BYREF

  v76[0] = -2;
  v75 = 0;
  v5 = *a2;
  v71 = v5;
  if ( v5 != nullptr )
    _InterlockedIncrement(v5 + 2);
  v6 = (char *)(a1 + 2000);
  v72 = (char *)(a1 + 2000);
  v73 = 4;
  v74 = (char *)(a1 + 2004);
  if ( v71 != nullptr )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v6, a3: 4);
    v72 = (char *)(a1 + 1996);
    v73 = 4;
    v74 = v6;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 1996,
      a3: 4);
    v72 = (char *)(a1 + 2004);
    v73 = 4;
    v69 = (char *)(a1 + 2008);
    v74 = (char *)(a1 + 2008);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 2004,
      a3: 4);
    v72 = (char *)(a1 + 2225);
    v73 = 1;
    v70 = (char *)(a1 + 2226);
    v74 = (char *)(a1 + 2226);
    v7 = *(_QWORD *)v71;
    v67 = (char *)(a1 + 2225);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(v7 + 40))(a1: v71, a2: a1 + 2225, a3: 1);
    v72 = (char *)(a1 + 2068);
    v73 = 36;
    v74 = (char *)(a1 + 2104);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 2068,
      a3: 36);
    v72 = (char *)(a1 + 2108);
    v73 = 4;
    v63 = a1 + 2112;
    v74 = (char *)(a1 + 2112);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 2108,
      a3: 4);
    v72 = (char *)(a1 + 2230);
    v73 = 1;
    v62 = a1 + 2231;
    v74 = (char *)(a1 + 2231);
    v56 = (char *)(a1 + 2230);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 2230,
      a3: 1);
    v72 = (char *)(a1 + 2104);
    v73 = 4;
    v74 = (char *)(a1 + 2108);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 2104,
      a3: 4);
    v8 = a1 + 2040;
    v72 = (char *)(a1 + 2040);
    v73 = 8;
    v9 = (char *)(a1 + 2048);
    v74 = (char *)(a1 + 2048);
    v10 = a1 + 2064;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 2040,
      a3: 8);
    v72 = (char *)(a1 + 2064);
    v73 = 4;
    v74 = (char *)(a1 + 2068);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 2064,
      a3: 4);
  }
  else
  {
    v69 = (char *)(a1 + 2008);
    v67 = (char *)(a1 + 2225);
    v70 = (char *)(a1 + 2226);
    v63 = a1 + 2112;
    v56 = (char *)(a1 + 2230);
    v74 = nullptr;
    v73 = 0;
    v72 = nullptr;
    v62 = a1 + 2231;
    v8 = a1 + 2040;
    v9 = (char *)(a1 + 2048);
    v10 = a1 + 2064;
  }
  v74 = nullptr;
  v73 = 0;
  v72 = nullptr;
  if ( (unsigned __int8)sub_141478210(a1: a1 + 592, a2: &v71) == 0 )
    goto LABEL_58;
  v57 = (char *)v8;
  if ( v73 != 0 && v71 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v72);
  v74 = nullptr;
  v73 = 0;
  v72 = nullptr;
  if ( (unsigned __int8)sub_141478210(a1: a1 + 872, a2: &v71) == 0 )
    goto LABEL_58;
  if ( v73 != 0 && v71 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v72);
  v74 = nullptr;
  v73 = 0;
  v72 = nullptr;
  if ( (unsigned __int8)sub_141478210(a1: a1 + 1432, a2: &v71) == 0 )
    goto LABEL_58;
  if ( v73 != 0 && v71 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v72);
  v74 = nullptr;
  v73 = 0;
  v72 = nullptr;
  if ( (unsigned __int8)sub_141478210(a1: a1 + 1152, a2: &v71) == 0 )
    goto LABEL_58;
  v58 = v10;
  if ( v74 == (char *)(a1 + 2136) )
  {
    v11 = a1 + 2156;
    v12 = (char *)(a1 + 2016);
    v14 = v73 == -20;
    v13 = v73 + 20;
    v73 += 20;
    v74 = (char *)(a1 + 2156);
    if ( v14 )
    {
      v68 = (char *)(a1 + 2156);
      v15 = v71;
      v72 = (char *)(a1 + 2016);
      v73 = 4;
      v66 = (char *)(a1 + 2020);
      v74 = (char *)(a1 + 2020);
      if ( v71 != nullptr )
        goto LABEL_27;
      goto LABEL_29;
    }
  }
  else
  {
    if ( v73 != 0 && v71 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
        a1: v71,
        a2: v72,
        a3: v73);
    v72 = (char *)(a1 + 2136);
    v73 = 20;
    v11 = a1 + 2156;
    v74 = (char *)(a1 + 2156);
    v12 = (char *)(a1 + 2016);
    v13 = 20;
  }
  v15 = v71;
  if ( v71 != nullptr )
  {
    v68 = (char *)v11;
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: v72,
      a3: v13);
    v72 = v12;
    v73 = 4;
    v66 = (char *)(a1 + 2020);
    v74 = (char *)(a1 + 2020);
LABEL_27:
    v16 = *(_QWORD *)v15;
    v64 = v12;
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(v16 + 40))(a1: v15, a2: v12, a3: 4);
    v72 = v70;
    v73 = 2;
    v60 = (char *)(a1 + 2228);
    v74 = (char *)(a1 + 2228);
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: v70,
      a3: 2);
    v72 = v68;
    v73 = 4;
    v65 = (char *)(a1 + 2160);
    v74 = (char *)(a1 + 2160);
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: v68,
      a3: 4);
    v72 = (char *)(a1 + 1992);
    v73 = 4;
    v74 = (char *)(a1 + 1996);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: a1 + 1992,
      a3: 4);
    v72 = (char *)(a1 + 2212);
    v73 = 1;
    v74 = (char *)(a1 + 2213);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: a1 + 2212,
      a3: 1);
    v72 = (char *)(a1 + 2218);
    v73 = 1;
    v74 = (char *)(a1 + 2219);
    v59 = (char *)(a1 + 2218);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: a1 + 2218,
      a3: 1);
    v72 = (char *)(a1 + 2213);
    v73 = 3;
    v74 = (char *)(a1 + 2216);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: a1 + 2213,
      a3: 3);
    v72 = v69;
    v73 = 4;
    v68 = (char *)(a1 + 2012);
    v74 = (char *)(a1 + 2012);
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: v69,
      a3: 4);
    v72 = (char *)(a1 + 2176);
    v73 = 4;
    v74 = (char *)(a1 + 2180);
    v17 = *(_QWORD *)v15;
    v70 = (char *)(a1 + 2176);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(v17 + 40))(a1: v15, a2: a1 + 2176, a3: 4);
    v72 = (char *)(a1 + 2222);
    v73 = 3;
    v74 = v67;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: a1 + 2222,
      a3: 3);
    v72 = (char *)(a1 + 2216);
    v73 = 1;
    v69 = (char *)(a1 + 2217);
    v74 = (char *)(a1 + 2217);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: a1 + 2216,
      a3: 1);
    v72 = (char *)(a1 + 2180);
    v73 = 8;
    v18 = a1 + 2188;
    v74 = (char *)(a1 + 2188);
    v19 = (char *)(a1 + 2200);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: a1 + 2180,
      a3: 8);
    v72 = (char *)(a1 + 2200);
    v73 = 4;
    v74 = (char *)(a1 + 2204);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
      a1: v15,
      a2: a1 + 2200,
      a3: 4);
    v20 = 0;
    goto LABEL_30;
  }
  v66 = (char *)(a1 + 2020);
LABEL_29:
  v64 = v12;
  v65 = (char *)(a1 + 2160);
  v60 = (char *)(a1 + 2228);
  v59 = (char *)(a1 + 2218);
  v68 = (char *)(a1 + 2012);
  v70 = (char *)(a1 + 2176);
  v72 = (char *)(a1 + 2222);
  v73 = 3;
  v69 = (char *)(a1 + 2217);
  v18 = a1 + 2188;
  v19 = (char *)(a1 + 2200);
  v20 = 1;
  v15 = nullptr;
LABEL_30:
  v72 = (char *)(a1 + 2196);
  v73 = 4;
  v74 = v19;
  v21 = &v75;
  if ( v19 == &v75 )
  {
    v22 = 5;
    v21 = (char *)(a1 + 2196);
  }
  else
  {
    if ( v20 != 0 )
    {
      v15 = nullptr;
    }
    else
    {
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(
        a1: v15,
        a2: a1 + 2196,
        a3: 4);
      v15 = v71;
    }
    v72 = &v75;
    v22 = 1;
  }
  v67 = (char *)v18;
  v73 = v22;
  v74 = (char *)v76;
  if ( v15 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v15 + 40LL))(a1: v15, a2: v21);
  v74 = nullptr;
  v73 = 0;
  v72 = nullptr;
  if ( v75 > 0 )
  {
    if ( *(_QWORD *)(a1 + 560) != 0
      || (v23 = sub_1407E4940(),
          v24 = sub_1407E4490(a1: v23, a2: 496),
          sub_141758A10(a1: v24, a2: 0, a3: 496),
          *(_QWORD *)(a1 + 560) = v24,
          v75 > 0) )
    {
      v25 = 0;
      do
      {
        if ( dword_141B643A0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B643A0);
          if ( dword_141B643A0 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B64350,
              a2: 1100155842,
              a3: 1024,
              a4: 228,
              a5: 0,
              a6: 0,
              a7: 1024,
              a8: 0);
            sub_141751048(a1: sub_1414A6B00);
            sub_141750EA0(a1: &dword_141B643A0);
          }
        }
        v26 = sub_1407E58C0(a1: &unk_141B64350, a2: 228);
        sub_141758A10(a1: v26, a2: 0, a3: 228);
        if ( v73 != 0 && v71 != nullptr )
          (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v72);
        v74 = nullptr;
        v73 = 0;
        v72 = nullptr;
        if ( (unsigned __int8)sub_141478470(a1: v26, a2: &v71) == 0 )
          goto LABEL_58;
        v27 = *(unsigned __int8 **)(a1 + 560);
        v28 = *v27;
        if ( v28 <= 0x3B )
        {
          *(_QWORD *)&v27[8 * v28 + 8] = v26;
          *v27 = v28 + 1;
        }
        else
        {
          v29 = v27[488];
          if ( *(_QWORD *)&v27[8 * v29 + 8] != 0 )
            sub_1414A6D20();
          *(_QWORD *)&v27[8 * v29 + 8] = v26;
          v30 = v27[488] + 1;
          if ( v30 >= 0x3Cu )
            v30 = 0;
          v27[488] = v30;
        }
      }
      while ( ++v25 < v75 );
    }
  }
  sub_1414786C0(a1: &v61, a2: &v71, a3: a1 + 64);
  if ( (_DWORD)v61 != 0 )
  {
LABEL_58:
    v31 = 0;
    goto LABEL_59;
  }
  v34 = v67;
  if ( v74 == v67 )
  {
    v14 = v73 == -4;
    v38 = v73 + 4;
    v73 += 4;
    v74 = (char *)(a1 + 2192);
    v35 = (char *)v58;
    v36 = v57;
    v37 = v69;
    if ( v14 )
      goto LABEL_76;
  }
  else
  {
    v35 = (char *)v58;
    v36 = v57;
    v37 = v69;
    if ( v73 != 0 && v71 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
        a1: v71,
        a2: v72,
        a3: v73);
    v72 = v34;
    v73 = 4;
    v74 = (char *)(a1 + 2192);
    v38 = 4;
  }
  if ( v71 == nullptr )
  {
    v73 = 0;
    v72 = v37;
LABEL_81:
    v39 = nullptr;
    goto LABEL_82;
  }
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
    a1: v71,
    a2: v72,
    a3: v38);
LABEL_76:
  v72 = v37;
  v73 = 1;
  v74 = v59;
  if ( v71 == nullptr )
    goto LABEL_81;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v37, a3: 1);
  v72 = v66;
  v73 = 20;
  v74 = v36;
  if ( v71 == nullptr )
    goto LABEL_81;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v66, a3: 20);
  v72 = (char *)(a1 + 2192);
  v73 = 4;
  v74 = (char *)(a1 + 2196);
  if ( v71 == nullptr )
    goto LABEL_81;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
    a1: v71,
    a2: a1 + 2192,
    a3: 4);
  v39 = v71;
LABEL_82:
  v72 = (char *)(a1 + 2204);
  v73 = 4;
  v74 = (char *)(a1 + 2208);
  *(_WORD *)(a1 + 2219) = 0;
  *(_DWORD *)(a1 + 2164) = 0;
  *(_BYTE *)(a1 + 2221) = 0;
  if ( v39 == nullptr
    || ((*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v39 + 40LL))(
          a1: v39,
          a2: a1 + 2204,
          a3: 4),
        v72 = (char *)(a1 + 2128),
        v73 = 8,
        v74 = (char *)(a1 + 2136),
        v71 == nullptr) )
  {
    v41 = (char *)(a1 + 2124);
    v72 = nullptr;
LABEL_90:
    v42 = v70;
    goto LABEL_91;
  }
  v40 = v35;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
    a1: v71,
    a2: a1 + 2128,
    a3: 8);
  v41 = (char *)(a1 + 2124);
  v72 = (char *)(a1 + 2124);
  v73 = 4;
  v74 = (char *)(a1 + 2128);
  if ( v71 == nullptr )
    goto LABEL_90;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
    a1: v71,
    a2: a1 + 2124,
    a3: 4);
  v72 = v9;
  v73 = 4;
  v74 = (char *)(a1 + 2052);
  if ( v71 == nullptr )
    goto LABEL_90;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v9, a3: 4);
  v72 = v60;
  v73 = 2;
  v74 = v56;
  if ( v71 == nullptr )
    goto LABEL_90;
  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v60, a3: 2);
  v72 = (char *)(a1 + 2052);
  v73 = 12;
  v74 = v40;
  v42 = v70;
  if ( v71 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: a1 + 2052,
      a3: 12);
LABEL_91:
  v72 = (char *)(a1 + 2168);
  v73 = 8;
  v74 = v42;
  v43 = &v75;
  if ( v42 == &v75 )
  {
    v44 = 9;
    v43 = (char *)(a1 + 2168);
  }
  else
  {
    if ( v71 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v71 + 40LL))(
        a1: v71,
        a2: a1 + 2168,
        a3: 8);
    v72 = &v75;
    v44 = 1;
  }
  v73 = v44;
  v74 = (char *)v76;
  if ( v71 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v43);
  v74 = nullptr;
  v73 = 0;
  v72 = nullptr;
  sub_140893BE0(a1: a1 + 568, a2: v75);
  if ( v75 <= 0 )
  {
LABEL_105:
    v47 = v68;
    if ( v74 == v68 )
    {
      v14 = v73 == -4;
      v51 = v73 + 4;
      v73 += 4;
      v74 = v64;
      v48 = (char *)v62;
      v49 = (char *)v63;
      if ( v14 )
        goto LABEL_114;
    }
    else
    {
      v48 = (char *)v62;
      v49 = (char *)v63;
      v50 = v64;
      if ( v73 != 0 && v71 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
          a1: v71,
          a2: v72,
          a3: v73);
      v72 = v47;
      v73 = 4;
      v74 = v50;
      v51 = 4;
    }
    if ( v71 == nullptr )
    {
LABEL_117:
      v72 = v48;
      v73 = 1;
      v74 = (char *)(a1 + 2232);
      v52 = 1;
      if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDE9u )
      {
        v73 = 2;
        v74 = (char *)(a1 + 2233);
        v52 = 2;
      }
      if ( v71 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
          a1: v71,
          a2: v48,
          a3: v52);
      v74 = nullptr;
      v73 = 0;
      v72 = nullptr;
      LOBYTE(v53) = sub_141476E70(a1, a2: (__int64 *)&v71, a3);
      v31 = v53;
      goto LABEL_59;
    }
    (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
      a1: v71,
      a2: v72,
      a3: v51);
LABEL_114:
    v72 = v49;
    v73 = 12;
    v74 = v41;
    if ( v71 != nullptr )
    {
      (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
        a1: v71,
        a2: v49,
        a3: 12);
      v72 = v65;
      v73 = 4;
      v74 = (char *)(a1 + 2164);
      if ( v71 != nullptr )
        (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v71 + 40LL))(
          a1: v71,
          a2: v65,
          a3: 4);
    }
    goto LABEL_117;
  }
  v45 = 0;
  while ( 1 )
  {
    v46 = sub_141750CC0(a1: 24);
    *(_QWORD *)(v46 + 8) = 0;
    *(_DWORD *)(v46 + 16) = 0;
    strcpy((char *)(v46 + 20), "l\a");
    v61 = v46;
    if ( v73 != 0 && v71 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v72);
    v74 = nullptr;
    v73 = 0;
    v72 = nullptr;
    if ( (unsigned __int8)sub_141478DA0(a1: v46, a2: &v71) == 0 )
      break;
    sub_14087F540(a1: a1 + 568, a2: &v61);
    if ( ++v45 >= v75 )
      goto LABEL_105;
  }
  sub_141750CFC(a1: v46);
  v31 = 0;
LABEL_59:
  if ( v73 != 0 )
  {
    if ( v71 == nullptr )
      return v31;
    (*(void (__fastcall **)(volatile signed __int32 *, char *))(*(_QWORD *)v71 + 40LL))(a1: v71, a2: v72);
  }
  v32 = v71;
  v74 = nullptr;
  v73 = 0;
  v72 = nullptr;
  if ( v71 != nullptr && _InterlockedDecrement(v71 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v32)(a1: v32, a2: 1);
  return v31;
}
