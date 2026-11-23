bool __fastcall sub_14432A580(_BYTE *a1, _QWORD *a2, unsigned __int16 a3)
{
  _BYTE *v6; // rdi
  __int64 v7; // r8
  __int64 *v8; // r15
  _BYTE *v9; // r14
  _BYTE *v10; // rbx
  __int64 v11; // r8
  _BYTE *v12; // rdi
  _QWORD *v13; // rbp
  _BYTE *v14; // rax
  __int64 v15; // r8
  __int64 v16; // r8
  __int64 v17; // r8
  _BYTE *v19; // [rsp+20h] [rbp-48h]

  v6 = a1 + 8;
  v7 = a2[2];
  if ( (_BYTE *)a2[3] == a1 + 8 )
  {
    v8 = a2 + 2;
    v9 = a1 + 9;
    v10 = a1 + 10;
    v11 = v7 + 1;
    a2[2] = v11;
    a2[3] = a1 + 9;
    if ( v11 == 0 )
      goto LABEL_9;
  }
  else
  {
    if ( v7 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1]);
    a2[1] = v6;
    v8 = a2 + 2;
    a2[2] = 1;
    v9 = a1 + 9;
    a2[3] = a1 + 9;
    v10 = a1 + 10;
    v11 = 1;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1], a3: v11);
LABEL_9:
  v19 = v6;
  a2[1] = v10;
  a2[2] = 2;
  v12 = a1 + 12;
  a2[3] = a1 + 12;
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v10, a3: 2);
  v13 = a2 + 1;
  a2[1] = v9;
  a2[2] = 1;
  a2[3] = v10;
  *v12 = 0;
  v14 = (_BYTE *)a2[3];
  if ( a3 < 0xDCDu )
  {
    if ( v14 == a1 )
    {
      v17 = a2[2] + 8LL;
      a2[2] = v17;
      a2[3] = v19;
      if ( a3 >= 0xDC4u )
      {
LABEL_34:
        if ( v17 == 0 )
          goto LABEL_37;
        goto LABEL_35;
      }
      if ( v17 == 0 )
      {
LABEL_32:
        a2[3] = 0;
        a2[2] = 0;
        *v13 = 0;
        if ( a1[11] != 9 )
          goto LABEL_37;
        a1[11] = 10;
        v17 = *v8;
        goto LABEL_34;
      }
LABEL_30:
      if ( *a2 != 0 )
        (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v13, a3: v17);
      goto LABEL_32;
    }
LABEL_26:
    if ( *v8 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v13);
    a2[1] = a1;
    a2[2] = 8;
    a2[3] = v19;
    v17 = 8;
    if ( a3 >= 0xDC4u )
      goto LABEL_35;
    goto LABEL_30;
  }
  v15 = *v8;
  if ( v14 == v12 )
  {
    v16 = v15 + 1;
    a2[2] = v16;
    a2[3] = a1 + 13;
    if ( v16 == 0 )
      goto LABEL_24;
  }
  else
  {
    if ( v15 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v13);
    a2[1] = v12;
    a2[2] = 1;
    a2[3] = a1 + 13;
    v16 = 1;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v13, a3: v16);
LABEL_24:
  a2[3] = 0;
  a2[2] = 0;
  *v13 = 0;
  if ( *v12 != 1 )
    goto LABEL_26;
  a2[1] = a1;
  a2[2] = 4;
  a2[3] = a1 + 4;
  v17 = 4;
LABEL_35:
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v13, a3: v17);
LABEL_37:
  a2[3] = 0;
  a2[2] = 0;
  *v13 = 0;
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
