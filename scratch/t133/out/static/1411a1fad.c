__int64 __fastcall sub_1411A1F80(__int64 a1, _QWORD *a2, char a3)
{
  _BYTE *v6; // rsi
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rbx
  __int64 v23; // r12
  _QWORD *v24; // rbx
  __int64 v25; // rbx
  _QWORD *v26; // rax
  __int64 v27; // rbx
  __int64 v29; // rax
  _QWORD *v30; // rbx
  char v31; // [rsp+4Eh] [rbp-15Ah] BYREF
  char v32; // [rsp+4Fh] [rbp-159h] BYREF
  int v33; // [rsp+50h] [rbp-158h] BYREF
  char v34; // [rsp+57h] [rbp-151h] BYREF
  _BYTE v35[336]; // [rsp+58h] [rbp-150h] BYREF

  v6 = v35;
  sub_1411A01D0(a1: v35);
  if ( a1 != 0 )
  {
    v6 = *(_BYTE **)(a1 + 160);
    if ( v6 == nullptr )
    {
      if ( dword_141B61AF8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B61AF8);
        if ( dword_141B61AF8 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B61AA8,
            a2: 1100160132,
            a3: 1536,
            a4: 280,
            a5: 0,
            a6: 0,
            a7: 1536,
            a8: 4096);
          sub_141751048(a1: sub_1411BEF70);
          sub_141750EA0(a1: &dword_141B61AF8);
        }
      }
      v6 = (_BYTE *)sub_1407E58C0(a1: &unk_141B61AA8, a2: 280);
      sub_1411A01D0(a1: v6);
      *(_QWORD *)(a1 + 160) = v6;
    }
  }
  LOBYTE(a1) = 1;
  if ( a3 != 0 )
  {
    v7 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 216, a3: 4);
    if ( *(_DWORD *)(v7 + 16) != 0 )
      goto LABEL_39;
    v8 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v34, a3: 1);
    if ( *(_DWORD *)(v8 + 16) != 0 )
      goto LABEL_39;
    v6[269] = v34;
    v9 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 264, a3: 1);
    if ( *(_DWORD *)(v9 + 16) != 0 )
      goto LABEL_39;
    v10 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 265, a3: 1);
    if ( *(_DWORD *)(v10 + 16) != 0 )
      goto LABEL_39;
    v11 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 266, a3: 1);
    if ( *(_DWORD *)(v11 + 16) != 0 )
      goto LABEL_39;
    v12 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 256, a3: 2);
    if ( *(_DWORD *)(v12 + 16) != 0 )
      goto LABEL_39;
    v13 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 258, a3: 2);
    if ( *(_DWORD *)(v13 + 16) != 0 )
      goto LABEL_39;
    v14 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 262, a3: 2);
    if ( *(_DWORD *)(v14 + 16) != 0 )
      goto LABEL_39;
    v15 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 260, a3: 2);
    if ( *(_DWORD *)(v15 + 16) != 0 )
      goto LABEL_39;
    v16 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 267, a3: 1);
    if ( *(_DWORD *)(v16 + 16) != 0 )
      goto LABEL_39;
    v17 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 248, a3: 2);
    if ( *(_DWORD *)(v17 + 16) != 0 )
      goto LABEL_39;
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 250, a3: 2);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      goto LABEL_39;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 252, a3: 2);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      goto LABEL_39;
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 254, a3: 2);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      goto LABEL_39;
    if ( (unsigned __int8)sub_140DB8980(a1: v6 + 228, a2) == 0 )
      goto LABEL_39;
    if ( (unsigned __int8)sub_140DB8980(a1: v6 + 232, a2) == 0 )
      goto LABEL_39;
    if ( (unsigned __int8)sub_140DB8980(a1: v6 + 236, a2) == 0 )
      goto LABEL_39;
    if ( (unsigned __int8)sub_140DB8980(a1: v6 + 240, a2) == 0 )
      goto LABEL_39;
    if ( (unsigned __int8)sub_140DB8980(a1: v6 + 244, a2) == 0 )
      goto LABEL_39;
    sub_1411A2530(a1: &v33, a2, a3: v6 + 128);
    if ( v33 != 0 )
      goto LABEL_39;
    sub_14096E360(a1: &v33, a2, a3: v6 + 104);
    if ( v33 != 0 )
      goto LABEL_39;
    if ( (unsigned __int8)sub_140DB8980(a1: v6 + 224, a2) == 0 )
      goto LABEL_39;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6 + 268, a3: 1);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      goto LABEL_39;
    v22 = *a2;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v33, a3: 2);
    if ( *(_DWORD *)(v22 + 16) != 0 )
      goto LABEL_39;
    if ( (_WORD)v33 != 0 )
    {
      sub_1413CB290(a1: v6 + 160);
      if ( (_WORD)v33 != 0 )
      {
        v23 = 0;
        do
        {
          v24 = (_QWORD *)sub_1409329B0(a1: 24);
          *v24 = 0x76C0001076C0001LL;
          v24[1] = 0x76C0001076C0001LL;
          v24[2] = -16580608;
          if ( (unsigned __int8)sub_1413CAE90(a1: v24, a2) == 0 )
            goto LABEL_39;
          sub_1409F6F40(a1: v6 + 160, a2: v24);
        }
        while ( ++v23 < (unsigned __int64)(unsigned __int16)v33 );
      }
    }
    v32 = 0;
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v32, a3: 1);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      goto LABEL_39;
    if ( v32 != 0 )
    {
      v26 = (_QWORD *)sub_1411A2610();
      *v26 = 0;
      v26[1] = 0;
      *(_QWORD *)((char *)v26 + 14) = 0;
      *((_QWORD *)v6 + 26) = v26;
      if ( (unsigned __int8)sub_14152F720(a1: v26, a2, a3: &qword_141B5FDA8) == 0 )
        goto LABEL_39;
    }
    v31 = 0;
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v31, a3: 1);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      goto LABEL_39;
    if ( v31 != 0 )
    {
      v29 = sub_1407E4940();
      v30 = (_QWORD *)sub_1407E4490(a1: v29, a2: 24);
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = sub_1407E4940();
      v30[2] = 0;
      v30[1] = 0;
      *v30 = 0;
      *((_QWORD *)v6 + 21) = v30;
      if ( (unsigned __int8)sub_1415BA3D0(a1: v30, a2) == 0 )
        goto LABEL_39;
    }
    if ( (unsigned __int8)sub_1409F66A0(a1: v6 + 152, a2) == 0 || (unsigned __int8)sub_1409FA1E0(a1: v6 + 270, a2) == 0 )
LABEL_39:
      LODWORD(a1) = 0;
  }
  sub_1411A04D0(a1: v35);
  return (unsigned int)a1;
}
