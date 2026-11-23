__int64 __fastcall sub_140047520(__int64 a1, int a2)
{
  __int64 v3; // rax
  int v4; // ebx
  __int64 *v5; // rbp
  char v6; // bl
  volatile signed __int32 *v7; // rcx
  __int64 **v8; // rax
  _QWORD *v9; // rax
  volatile signed __int32 *v10; // rsi
  __int64 v11; // rax
  __int64 v12; // r12
  int v13; // esi
  __int64 v14; // rsi
  int v15; // eax
  __int64 v16; // rsi
  __int64 v17; // rdi
  int v18; // eax
  char v19; // bl
  __int64 v20; // rax
  _QWORD *v21; // rax
  __int64 v22; // rsi
  char v23; // bl
  _QWORD *v24; // rax
  __int64 v25; // rsi
  __int64 v26; // rdi
  __int64 v27; // r8
  int v28; // ebx
  __int64 v29; // r15
  __int64 v30; // rsi
  __int64 v31; // rax
  __int64 v32; // rax
  __int64 v33; // rdx
  __int64 v34; // r8
  __int64 v35; // rsi
  __int64 v36; // r8
  __int64 v37; // rsi
  char v38; // bl
  __int64 v39; // rsi
  __int64 v40; // rax
  __int64 v41; // rcx
  char v42; // bl
  volatile signed __int32 *v43; // rcx
  _QWORD *v44; // rax
  __int64 v45; // rsi
  volatile signed __int32 *v46; // rsi
  volatile signed __int32 *v47; // rcx
  __int64 v49; // rsi
  volatile signed __int32 *v50; // [rsp+60h] [rbp-B8h] BYREF
  volatile signed __int32 *v51; // [rsp+68h] [rbp-B0h] BYREF
  __int64 v52; // [rsp+70h] [rbp-A8h] BYREF
  int v53; // [rsp+78h] [rbp-A0h]
  volatile signed __int32 *v54; // [rsp+80h] [rbp-98h] BYREF
  char v55[8]; // [rsp+88h] [rbp-90h] BYREF
  __int64 v56; // [rsp+90h] [rbp-88h]
  __int64 v57; // [rsp+98h] [rbp-80h]
  __int64 v58; // [rsp+A0h] [rbp-78h] BYREF
  volatile signed __int32 *v59; // [rsp+A8h] [rbp-70h] BYREF
  _BYTE v60[16]; // [rsp+B0h] [rbp-68h] BYREF
  _BYTE v61[16]; // [rsp+C0h] [rbp-58h] BYREF
  int v62[18]; // [rsp+D0h] [rbp-48h] BYREF

  v56 = a1;
  v3 = qword_141ABD830;
  *(_DWORD *)(qword_141ABD830 + 1380) = 0;
  *(_BYTE *)(v3 + 1355) = 0;
  v57 = v3;
  *(_WORD *)(v3 + 1353) = 256;
  sub_14083D2C0(a1: v61);
  v4 = qword_141ABDFE8;
  v5 = &v52;
  sub_14083D6D0(a1: &v52, a2: 0);
  if ( (unsigned __int8)sub_1408008F0(
                          a1: v4,
                          a2: (unsigned int)&unk_141ABFD60,
                          a3: (unsigned int)v61,
                          a4: (unsigned int)&v52,
                          a5: 0) != 0 )
  {
    v6 = sub_14083E0B0(a1: v61);
    sub_14083D320(a1: &v52);
    LOBYTE(v5) = 1;
    if ( v6 != 0 )
      goto LABEL_85;
  }
  else
  {
    sub_14083D320(a1: &v52);
  }
  sub_1407D5DC0(a1: qword_141ABD878, a2: &v51, a3: &qword_141B597F0);
  if ( v51 == nullptr )
  {
LABEL_22:
    if ( v51 == nullptr )
      goto LABEL_11;
LABEL_23:
    sub_140310A50(a1: v55);
    sub_14083D2C0(a1: v60);
    if ( (unsigned __int8)sub_1408008F0(
                            a1: qword_141ABDFE8,
                            a2: (unsigned int)&unk_141ABFD18,
                            a3: (unsigned int)v60,
                            a4: (unsigned int)&qword_141B5A4A0,
                            a5: 0) != 0 )
    {
      sub_14083E100(a1: v60, a2: &v52);
      sub_140809170(a1: v55, a2: &v52);
      sub_140808B00(a1: &v52);
    }
    v54 = nullptr;
    v10 = v51;
    sub_1407D8AB0(a1: &v52, a2: 0x1418E2C24LL);
    (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64 *, __int64 *, volatile signed __int32 **, int))(*(_QWORD *)v10 + 216LL))(
      a1: v10,
      a2: &v50,
      a3: &qword_141B59758,
      a4: &v52,
      a5: &v54,
      a6: 1);
    LOBYTE(v5) = 1;
    if ( v54 != nullptr )
    {
      v11 = sub_1407D4670();
      if ( v11 != 0 )
      {
        v12 = v11;
        v56 += 44640;
        LOBYTE(v5) = 1;
        do
        {
          sub_1407D46A0(a1: v54, a2: &v50, a3: --v12);
          v13 = 4;
          if ( (unsigned __int8)sub_140047E50(a1: 0) == 0 )
          {
            v14 = sub_140809850(a1: &qword_141B59EE0);
            v15 = sub_140310DB0(a1: &qword_141B59EE0);
            v52 = v14;
            v53 = v15;
            if ( (unsigned __int8)sub_14080B890(a1: v55, a2: &v52) != 0 )
              goto LABEL_32;
            (*(void (__fastcall **)(volatile signed __int32 *, int *))(*(_QWORD *)v50 + 16LL))(a1: v50, a2: v62);
            v16 = sub_1400015F0(a1: v62);
            v17 = sub_140809850(a1: v16);
            v18 = sub_140310DB0(a1: v16);
            v52 = v17;
            v53 = v18;
            v19 = sub_14080B890(a1: v55, a2: &v52);
            sub_140808B00(a1: v62);
            v13 = 5;
            if ( v19 != 0 )
            {
LABEL_32:
              (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v50 + 16LL))(a1: v50, a2: &v52);
              v20 = sub_1400015F0(a1: &v52);
              sub_140809100(a1: v56, a2: v20);
              sub_140808B00(a1: &v52);
              if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
              {
                v21 = &unk_141ABD978;
                while ( 1 )
                {
                  v21 = (_QWORD *)v21[2];
                  if ( v21 == nullptr || *v21 == 0 )
                    break;
                  if ( (*((_BYTE *)v21 + 28) & 1) == 0 || *((int *)v21 + 6) > 1 )
                    goto LABEL_42;
                }
                v22 = sub_1407E2C90(a1: 2160);
                sub_1407E2EB0(a1: v22, a2: 1099914335, a3: 18278, a4: 1099839256, a5: 0, a6: 1);
                sub_1407E0010(a1: v22, a2: 0x14193ADD1LL);
                if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v22) & 4) != 0 )
                  sub_1407CD750();
              }
LABEL_42:
              (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v50 + 24LL))(a1: v50, a2: &v52);
              (*(void (__fastcall **)(volatile signed __int32 *, int *))(*(_QWORD *)v50 + 16LL))(a1: v50, a2: v62);
              v59 = v51;
              if ( v51 != nullptr )
                _InterlockedIncrement(v51 + 2);
              v23 = sub_1400959F0(a1: v57, a2: &v59, a3: v62, a4: &v52);
              sub_140808B00(a1: v62);
              if ( v23 != 0 )
              {
                if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
                {
                  v24 = &unk_141ABD978;
                  while ( 1 )
                  {
                    v24 = (_QWORD *)v24[2];
                    if ( v24 == nullptr || *v24 == 0 )
                      break;
                    if ( (*((_BYTE *)v24 + 28) & 1) == 0 || *((int *)v24 + 6) > 1 )
                      goto LABEL_56;
                  }
                  v28 = a2;
                  v29 = sub_1407E2C90(a1: 2160);
                  sub_1407E2EB0(a1: v29, a2: 1099914335, a3: 18281, a4: 1099839256, a5: 0, a6: 1);
                  v30 = sub_1407E0010(a1: v29, a2: 0x141941498LL);
                  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v50 + 16LL))(
                    a1: v50,
                    a2: &v52);
                  v31 = sub_1407D6070(a1: v30, a2: &v52);
                  v32 = sub_1407E0010(a1: v31, a2: 0x14194126CLL);
                  sub_1407DFB20(a1: v32, a2: (unsigned __int16)word_141AAA412);
                  sub_140808B00(a1: &v52);
                  v33 = v29;
                  a2 = v28;
                  if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v33) & 4) != 0 )
                    sub_1407CD750();
                }
LABEL_56:
                if ( sub_140F7B2A0() != 0 )
                {
                  v35 = qword_141B5AD60;
                  v52 = 0;
                  sub_140809040(a1: &v52, a2: 0x14191932ELL, a3: 0xFFFFFFFFLL);
                  LOBYTE(v36) = 1;
                  (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v35 + 120LL))(
                    a1: v35,
                    a2: &v52,
                    a3: v36,
                    a4: 0);
                  sub_140808B00(a1: &v52);
                }
                LOWORD(v34) = 1460;
                sub_140DB8850(a1: &dword_141AAE084, a2: v62, a3: v34);
                v37 = qword_141ABDFE8;
                sub_14083D6D0(a1: &v52, a2: 0);
                v38 = sub_140800A10(a1: v37, a2: &unk_141ABFD28, a3: &v52, a4: 0);
                sub_14083D320(a1: &v52);
                if ( v38 != 0 )
                {
                  v39 = v57;
                  sub_140095380(a1: v57);
                  sub_140094BE0(a1: v39);
                }
                (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v50 + 16LL))(
                  a1: v50,
                  a2: &v52);
                v40 = sub_1400015F0(a1: &v52);
                v42 = sub_14003EC00(
                        a1: v41,
                        a2: 0,
                        a3: (__int64)&qword_141B59EE0,
                        a4: v62,
                        a5: nullptr,
                        a6: 0x1418761ECLL,
                        a7: (_DWORD *)0x1418761ECLL,
                        a8: 0,
                        a9: 0,
                        a10: v40,
                        a11: (__int64)&qword_141B59EE0);
                sub_140808B00(a1: &v52);
                LODWORD(v5) = (unsigned __int8)v5;
                if ( v42 == 0 )
                  LODWORD(v5) = 0;
              }
              else
              {
                v25 = qword_141B5AD60;
                (*(void (__fastcall **)(volatile signed __int32 *, int *))(*(_QWORD *)v50 + 16LL))(a1: v50, a2: v62);
                v26 = sub_1400015F0(a1: v62);
                v58 = 0;
                sub_140809040(a1: &v58, a2: 0x1419414A7LL, a3: 0xFFFFFFFFLL);
                sub_140809550(a1: &v58, a2: &v52, a3: v26);
                LODWORD(v5) = 0;
                LOBYTE(v27) = 1;
                (*(void (__fastcall **)(__int64, __int64 *, __int64, _QWORD))(*(_QWORD *)v25 + 120LL))(
                  a1: v25,
                  a2: &v52,
                  a3: v27,
                  a4: 0);
                sub_140808B00(a1: &v52);
                sub_140808B00(a1: &v58);
                sub_140808B00(a1: v62);
              }
              v13 = 4 * ((unsigned __int8)a2 & (((unsigned __int8)v5 & 1) == 0));
            }
          }
          v43 = v50;
          if ( v50 != nullptr && _InterlockedDecrement(v50 + 2) == 0 )
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v43)(a1: v43, a2: 1);
        }
        while ( (v13 == 5 || v13 == 0) && v12 != 0 );
      }
    }
    if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
    {
      v44 = &unk_141ABD978;
      while ( 1 )
      {
        v44 = (_QWORD *)v44[2];
        if ( v44 == nullptr || *v44 == 0 )
          break;
        if ( (*((_BYTE *)v44 + 28) & 1) == 0 || *((int *)v44 + 6) > 1 )
          goto LABEL_78;
      }
      v45 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v45, a2: 1099914335, a3: 18311, a4: 1099839256, a5: 0, a6: 1);
      sub_1407E0010(a1: v45, a2: 0x1418E372BLL);
      if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v45) & 4) != 0 )
        sub_1407CD750();
    }
LABEL_78:
    v46 = v54;
    if ( v54 != nullptr && _InterlockedDecrement(v54) == 0 )
    {
      sub_1400532D0(a1: v46);
      sub_141750CFC(a1: v46);
    }
    sub_14083D320(a1: v60);
    sub_140808B00(a1: v55);
    goto LABEL_82;
  }
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, void *, __int64 *))(*(_QWORD *)v51 + 208LL))(
    a1: v51,
    a2: &v52,
    a3: &unk_141ABD900,
    a4: &qword_141B59858);
  v7 = v51;
  v8 = (__int64 **)v52;
  if ( v51 == (volatile signed __int32 *)v52 )
  {
    if ( v52 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v52 + 8)) == 0 )
    {
      v5 = *v8;
      ((void (__fastcall *)(__int64 **, __int64))**v8)(a1: v8, a2: 1);
    }
    goto LABEL_22;
  }
  if ( v51 != nullptr && _InterlockedDecrement(v51 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v7)(a1: v7, a2: 1);
  v51 = (volatile signed __int32 *)v52;
  if ( v52 != 0 )
    goto LABEL_23;
LABEL_11:
  LOBYTE(v5) = 1;
  if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
  {
    v9 = &unk_141ABD978;
    while ( 1 )
    {
      v9 = (_QWORD *)v9[2];
      if ( v9 == nullptr || *v9 == 0 )
        break;
      if ( (*((_BYTE *)v9 + 28) & 1) == 0 || *((int *)v9 + 6) > 1 )
        goto LABEL_82;
    }
    v49 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v49, a2: 1099914335, a3: 18242, a4: 1099839256, a5: 0, a6: 1);
    sub_1407E0010(a1: v49, a2: 0x1418F3660LL);
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v49) & 4) != 0 )
      sub_1407CD750();
  }
LABEL_82:
  v47 = v51;
  if ( v51 != nullptr && _InterlockedDecrement(v51 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v47)(a1: v47, a2: 1);
LABEL_85:
  sub_14083D320(a1: v61);
  return (unsigned int)v5;
}
