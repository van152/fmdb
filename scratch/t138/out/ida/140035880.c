__int64 __fastcall sub_140035880(__int64 a1, _QWORD *a2, char a3, unsigned __int8 a4, char a5, char a6, char a7)
{
  __int64 v11; // rdx
  int v12; // r8d
  int v13; // r9d
  __int64 v14; // rsi
  unsigned __int16 v15; // ax
  int v16; // r8d
  __int16 v17; // dx
  unsigned __int64 v18; // rsi
  _QWORD *v19; // rbp
  _QWORD *v20; // rax
  int v21; // r8d
  int v22; // r9d
  __int64 v23; // rsi
  char v24; // bl
  int v25; // r8d
  int v26; // r9d
  void (__fastcall ***v27)(_QWORD, __int64); // rcx
  __int64 v28; // rax
  unsigned __int64 v29; // rsi
  __int64 v30; // rbx
  __int64 v31; // rsi
  int v33; // [rsp+28h] [rbp-D0h]
  unsigned __int8 v34; // [rsp+6Bh] [rbp-8Dh]
  __int16 v35; // [rsp+6Ch] [rbp-8Ch] BYREF
  __int16 v36; // [rsp+6Eh] [rbp-8Ah] BYREF
  _BYTE v37[16]; // [rsp+70h] [rbp-88h] BYREF
  _BYTE v38[8]; // [rsp+80h] [rbp-78h] BYREF
  _QWORD v39[2]; // [rsp+88h] [rbp-70h] BYREF
  _BYTE v40[8]; // [rsp+98h] [rbp-60h] BYREF
  _BYTE v41[88]; // [rsp+A0h] [rbp-58h] BYREF

  if ( a5 == 0 )
    sub_14000E230(a1);
  (*(void (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 760LL))(a1: qword_141B5AD60);
  sub_1407C9510(a1: v41);
  sub_140F4BD10(a1: a2, a2: v41);
  sub_140809040(a1: a1 + 44520, a2: 0x141900162LL, a3: 0xFFFFFFFFLL);
  if ( (unsigned __int8)sub_140835E00(a1: v41, a2: 1718444900) != 0 )
  {
    v11 = 0x14191E84CLL;
  }
  else
  {
    if ( (unsigned __int8)sub_140835E00(a1: v41, a2: 1718447460) == 0 )
      goto LABEL_8;
    v11 = 0x1418FFDD7LL;
  }
  sub_140809040(a1: a1 + 44520, a2: v11, a3: 0xFFFFFFFFLL);
LABEL_8:
  v36 = 0;
  LOBYTE(v12) = 1;
  LOBYTE(v13) = 1;
  sub_140F4DBE0(
    a1: (unsigned int)&qword_141B5FDA8,
    (_DWORD)a2,
    a3: v12,
    a4: v13,
    a5: (__int64)&v36,
    a6: (__int64)sub_14011C380);
  sub_14011BE90(a1, a2: 0, a3: v36, a4: 0, a5: (__int64)&qword_141B59EE0, a6: 0);
  v14 = qword_141ABD830;
  v15 = sub_140FC9BB0();
  v17 = 3;
  if ( (unsigned __int16)(23593 * v15) < 0xA3Eu )
    v17 = 15;
  *(_DWORD *)(v14 + 1264) = ((unsigned __int16)(v15 & v17) == 0) + (v15 << 16) + 152;
  v35 = 0;
  LOBYTE(v16) = 1;
  if ( (unsigned __int8)sub_140F4DBE0(
                          a1: (unsigned int)&qword_141B5FDA8,
                          (_DWORD)a2,
                          a3: v16,
                          a4: 0,
                          a5: (__int64)&v35,
                          a6: (__int64)sub_14011C380) != 0 )
  {
    v18 = sub_140F617F0();
    byte_141A80840 = v18 < sub_140F601E0();
    if ( a3 != 0 )
    {
      v34 = a4;
      sub_140F62A50(a1: 0);
      LODWORD(v19) = 0;
      while ( (unsigned __int8)sub_140F62A70() == 0 )
      {
        v37[0] = 0;
        if ( (unsigned __int8)sub_140F64530(
                                a1: (unsigned int)&qword_141B5FDA8,
                                (_DWORD)a2,
                                a3: 0,
                                a4: (unsigned int)v37,
                                a5: 1,
                                a6: (__int64)sub_14011C380,
                                a7: 0) == 0 )
          goto LABEL_51;
      }
    }
    else
    {
      LOBYTE(v33) = 1;
      sub_140F500A0(
        a1: (unsigned int)&qword_141B5FDA8,
        (_DWORD)a2,
        a3: (unsigned int)&unk_141B5E460,
        a4: 0,
        a5: 0,
        a6: v33,
        a7: 0);
      if ( a7 != 0 )
      {
        LOBYTE(v21) = 1;
        LOBYTE(v22) = 1;
        if ( (unsigned __int8)sub_140F51450(a1: (unsigned int)&qword_141B5FDA8, (_DWORD)a2, a3: v21, a4: v22, a5: 0) == 0 )
        {
          LODWORD(v19) = 0;
          goto LABEL_51;
        }
        sub_140F3E690(a1: &qword_141B5FDA8, a2: 0);
      }
      v34 = a4;
      v35 = 0;
      sub_140F566E0(a1: (unsigned int)&qword_141B5FDA8, (_DWORD)a2, a3: 0, a4: (unsigned int)&v35, a5: 0, a6: 0);
      if ( a6 != 0 )
        sub_140F3C890(a1: &qword_141B5FDA8, a2: 0);
    }
    sub_14083D2C0(a1: v37);
    if ( (unsigned __int8)sub_140800D80(a1: qword_141ABDFE8, a2: &unk_141B5E3E0, a3: v37) == 0
      || (v23 = qword_141ABD468,
          sub_14083E100(a1: v37, a2: v39),
          v24 = sub_140823990(a1: v23, a2: v39),
          sub_140808B00(a1: v39),
          v24 == 0) )
    {
      sub_140823980(a1: qword_141ABD468, a2: v38);
      sub_14083DA50(a1: v39, a2: v38);
      sub_14083DFA0(a1: v37, a2: v39);
      sub_14083D320(a1: v39);
    }
    v39[0] = 0;
    sub_14083E100(a1: v37, a2: v40);
    sub_1407D8AC0(a1: v38, a2: v40);
    sub_140F50EC0(
      a1: (unsigned int)&qword_141B5FDA8,
      a2: (unsigned int)v38,
      a3: (unsigned int)v39,
      a4: 0,
      a5: 1,
      a6: 0,
      a7: 1,
      a8: 18);
    sub_140808B00(a1: v40);
    v27 = (void (__fastcall ***)(_QWORD, __int64))v39[0];
    if ( v39[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39[0] + 8LL)) == 0 )
      (**v27)(a1: v27, a2: 1);
    if ( a7 == 0 || a3 != 0 )
    {
      LOBYTE(v25) = 1;
      LOBYTE(v26) = 1;
      if ( (unsigned __int8)sub_140F51450(a1: (unsigned int)&qword_141B5FDA8, (_DWORD)a2, a3: v25, a4: v26, a5: a3) == 0 )
      {
        LODWORD(v19) = 0;
LABEL_50:
        sub_14083D320(a1: v37);
        goto LABEL_51;
      }
      sub_140F3E690(a1: &qword_141B5FDA8, a2: 0);
    }
    sub_140F59C40(a1: &qword_141B5FDA8, a2: v34);
    sub_14083E100(a1: v37, a2: v38);
    v19 = v39;
    sub_1407D8AC0(a1: v39, a2: v38);
    sub_140F50EC0(
      a1: (unsigned int)&qword_141B5FDA8,
      a2: (unsigned int)v39,
      a3: (_DWORD)a2,
      a4: 0,
      a5: 1,
      a6: 1,
      a7: 0,
      a8: 18);
    sub_140808B00(a1: v38);
    sub_14011C160(a1);
    if ( a5 != 0 )
    {
      if ( *(_BYTE *)(a1 + 417) == 0 )
      {
        sub_140054D70(
          a1: *(_QWORD *)(a1 + 392),
          a2: *(_QWORD *)(a1 + 400),
          a3: (__int64)(*(_QWORD *)(a1 + 400) - *(_QWORD *)(a1 + 392)) >> 3,
          a4: sub_1400115D0);
        *(_WORD *)(a1 + 416) = 256;
      }
      v28 = *(_QWORD *)(a1 + 392);
      if ( *(_QWORD *)(a1 + 400) != v28 )
      {
        v29 = 0;
        do
        {
          sub_140F47AD0(
            a1: (unsigned int)&qword_141B5FDA8,
            a2: *(_DWORD *)(v28 + 8 * v29++) + 24,
            a3: 0,
            a4: 0,
            a5: 1,
            a6: 1,
            a7: 1,
            a8: 0,
            a9: 0,
            a10: 0,
            a11: 0,
            a12: 0);
          v28 = *(_QWORD *)(a1 + 392);
        }
        while ( v29 < (*(_QWORD *)(a1 + 400) - v28) >> 3 );
      }
    }
    *(_QWORD *)(a1 + 424) = 0;
    LOBYTE(v19) = 1;
    goto LABEL_50;
  }
  if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
  {
    v20 = &unk_141ABD978;
    while ( 1 )
    {
      v20 = (_QWORD *)v20[2];
      if ( v20 == nullptr || *v20 == 0 )
        break;
      if ( (*((_BYTE *)v20 + 28) & 1) == 0 || *((int *)v20 + 6) > 1 )
        goto LABEL_48;
    }
    v30 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v30, a2: 1099914335, a3: 20782, a4: 1100101012, a5: 0, a6: 1);
    v31 = sub_1407E0010(a1: v30, a2: 0x141941E1ALL);
    (*(void (__fastcall **)(_QWORD, _BYTE *))(*(_QWORD *)*a2 + 32LL))(a1: *a2, a2: v37);
    sub_1407D6070(a1: v31, a2: v37);
    sub_140808B00(a1: v37);
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v30) & 4) != 0 )
      sub_1407CD750();
  }
LABEL_48:
  sub_14011C160(a1);
  LODWORD(v19) = 0;
LABEL_51:
  sub_140833970(a1: v41);
  return (unsigned int)v19;
}
