bool __fastcall sub_14145D260(_BYTE *a1, _QWORD *a2)
{
  __int64 v4; // r8
  __int64 v5; // r8
  _BYTE *v6; // r14
  __int64 v7; // r8
  bool v8; // zf
  _QWORD *v9; // r13
  _BYTE *v10; // r15
  __int64 v11; // r8
  __int64 v12; // r8
  __int64 v13; // r8
  __int64 v14; // r8
  __int64 v15; // r8
  _BYTE *v16; // r14
  __int64 v17; // rax
  __int64 v18; // r8
  __int64 v20; // r8
  __int64 v21; // r8
  _BYTE *v22; // r12
  __int64 v23; // r8
  _BYTE *v24; // rdi
  __int64 v25; // r8
  __int64 v26; // rcx
  __int64 v27; // rcx
  __int64 v28; // rax
  char v29; // [rsp+2Ch] [rbp-3Ch] BYREF
  char v30; // [rsp+2Dh] [rbp-3Bh] BYREF
  char v31; // [rsp+2Eh] [rbp-3Ah] BYREF
  char v32; // [rsp+2Fh] [rbp-39h] BYREF
  _BYTE v33[56]; // [rsp+30h] [rbp-38h] BYREF

  v4 = a2[2];
  if ( (_BYTE *)a2[3] == a1 )
  {
    v5 = v4 + 4;
  }
  else
  {
    if ( v4 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1]);
    a2[1] = a1;
    v5 = 4;
  }
  a2[2] = v5 + 4;
  v6 = a1 + 8;
  a2[3] = a1 + 8;
  v32 = 0;
  if ( a1 + 8 == &v32 )
  {
    v8 = v5 == -5;
    v7 = v5 + 5;
    a2[2] = v7;
    a2[3] = v33;
    if ( v8 )
      goto LABEL_15;
  }
  else
  {
    if ( v5 != -4 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1], a3: v5 + 4);
    a2[1] = &v32;
    a2[2] = 1;
    a2[3] = v33;
    v7 = 1;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1], a3: v7);
LABEL_15:
  v9 = a2 + 1;
  a2[3] = 0;
  a2[2] = 0;
  a2[1] = 0;
  v10 = a1 + 31;
  a1[31] = v32 & 0x3F | a1[31] & 0xC0;
  v31 = 0;
  v11 = a2[2];
  if ( (char *)a2[3] == &v31 )
  {
    v12 = v11 + 1;
    a2[2] = v12;
    a2[3] = &v32;
    if ( v12 == 0 )
      goto LABEL_23;
  }
  else
  {
    if ( v11 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9);
    a2[1] = &v31;
    a2[2] = 1;
    a2[3] = &v32;
    v12 = 1;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9, a3: v12);
LABEL_23:
  a2[3] = 0;
  a2[2] = 0;
  *v9 = 0;
  *v10 = (v31 << 6) | *v10 & 0x3F;
  v13 = a2[2];
  if ( (_BYTE *)a2[3] == v6 )
  {
    v14 = v13 + 4;
  }
  else
  {
    if ( v13 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9);
    *v9 = v6;
    v14 = 4;
  }
  a2[2] = v14;
  a2[3] = a1 + 12;
  if ( (unsigned __int8)sub_1414E57A0(a1: a1 + 12, a2) == 0 )
    return false;
  v15 = a2[2];
  if ( (_BYTE *)a2[3] == a1 + 24 )
  {
    v17 = v15 + 2;
    a2[2] = v15 + 2;
    v16 = a1 + 26;
    a2[3] = a1 + 26;
    v29 = 0;
    if ( a1 + 26 == &v29 )
    {
      a2[2] = v15 + 3;
      a2[3] = &v30;
      if ( v15 == -3 )
        goto LABEL_45;
      goto LABEL_43;
    }
    if ( v15 == -2 )
      goto LABEL_41;
    goto LABEL_39;
  }
  if ( v15 != 0 && *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9);
  a2[1] = a1 + 24;
  a2[2] = 2;
  v16 = a1 + 26;
  a2[3] = a1 + 26;
  v29 = 0;
  v17 = 2;
  if ( a1 + 26 != &v29 )
  {
LABEL_39:
    if ( *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9, a3: v17);
LABEL_41:
    *v9 = &v29;
    v18 = 1;
    goto LABEL_42;
  }
  v18 = 3;
LABEL_42:
  a2[2] = v18;
  a2[3] = &v30;
LABEL_43:
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9);
LABEL_45:
  a2[3] = 0;
  a2[2] = 0;
  *v9 = 0;
  a1[28] = v29 & 0x7F | a1[28] & 0x80;
  v30 = 0;
  v20 = a2[2];
  if ( (char *)a2[3] == &v30 )
  {
    v21 = v20 + 1;
    a2[2] = v21;
    a2[3] = &v31;
    if ( v21 == 0 )
      goto LABEL_53;
  }
  else
  {
    if ( v20 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9);
    a2[1] = &v30;
    a2[2] = 1;
    a2[3] = &v31;
    v21 = 1;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9, a3: v21);
LABEL_53:
  v22 = a1 + 28;
  a2[3] = 0;
  a2[2] = 0;
  *v9 = 0;
  a1[28] = (v30 << 7) | a1[28] & 0x7F;
  v23 = a2[2];
  if ( (_BYTE *)a2[3] != a1 + 29 )
  {
    if ( v23 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v9);
    a2[1] = a1 + 29;
    a2[2] = 1;
    v24 = a1 + 30;
    a2[3] = v24;
    v25 = 1;
    goto LABEL_59;
  }
  v24 = a1 + 30;
  v25 = v23 + 1;
  a2[2] = v25;
  a2[3] = v24;
  if ( v25 != 0 )
LABEL_59:
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1], a3: v25);
  v26 = *a2;
  a2[1] = v16;
  a2[2] = 2;
  a2[3] = v22;
  (*(void (__fastcall **)(__int64, _BYTE *, __int64))(*(_QWORD *)v26 + 40LL))(a1: v26, a2: v16, a3: 2);
  v27 = *a2;
  a2[1] = v24;
  a2[2] = 1;
  a2[3] = v10;
  (*(void (__fastcall **)(__int64, _BYTE *, __int64))(*(_QWORD *)v27 + 40LL))(a1: v27, a2: v24, a3: 1);
  v28 = *a2;
  *v9 = 0;
  a2[2] = 0;
  a2[3] = 0;
  return *(_DWORD *)(v28 + 16) == 0;
}
