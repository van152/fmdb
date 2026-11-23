__int64 __fastcall sub_1414C4670(_BYTE *a1, _QWORD *a2)
{
  __int64 v4; // rdi
  __int64 v5; // rsi
  _BYTE *v6; // rbp
  _BYTE *v7; // r14
  char *v8; // r13
  char *v9; // rbx
  __int64 v10; // r12
  char *v11; // r15
  __int64 v12; // r12
  char v13; // cl
  char v15; // [rsp+26h] [rbp-42h] BYREF
  _BYTE v16[65]; // [rsp+27h] [rbp-41h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v16, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
  {
    LODWORD(v4) = 0;
    return (unsigned int)v4;
  }
  v5 = *a2;
  if ( v5 == 0 )
  {
    v6 = a1 + 24;
    v7 = a1 + 16;
    if ( v16[0] > 6u )
      goto LABEL_21;
    v11 = &v15;
    if ( a1 + 22 != &v15 )
    {
      v12 = 1;
LABEL_14:
      v13 = 0;
      goto LABEL_15;
    }
    v8 = a1 + 20;
LABEL_13:
    v12 = 3;
    v11 = v8;
    goto LABEL_14;
  }
  _InterlockedIncrement((volatile signed __int32 *)(v5 + 8));
  (*(void (__fastcall **)(__int64, _BYTE *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 25, a3: 1);
  v6 = a1 + 24;
  LODWORD(v4) = (_DWORD)a1 + 8;
  (*(void (__fastcall **)(__int64, _BYTE *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 22, a3: 3);
  v7 = a1 + 16;
  (*(void (__fastcall **)(__int64, _BYTE *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 8, a3: 8);
  v8 = a1 + 20;
  (*(void (__fastcall **)(__int64, _BYTE *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1, a3: 8);
  if ( v16[0] >= 7u )
  {
    v9 = a1 + 26;
    v10 = 2;
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: v8, a3: 2);
LABEL_20:
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: v9, a3: v10);
    goto LABEL_21;
  }
  v15 = 0;
  v11 = &v15;
  if ( a1 + 22 == &v15 )
    goto LABEL_13;
  (*(void (__fastcall **)(__int64, _BYTE *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 20, a3: 2);
  v12 = 1;
  v13 = 8;
  switch ( v15 )
  {
    case 17:
      break;
    case 20:
      v13 = 2;
      break;
    case 21:
      v13 = 4;
      break;
    case 22:
      v13 = 9;
      break;
    case 24:
      v13 = 3;
      break;
    case 33:
      v13 = 1;
      break;
    case 35:
      v13 = 6;
      break;
    case 36:
      v13 = 7;
      break;
    case 38:
      v13 = 5;
      break;
    default:
      goto LABEL_14;
  }
LABEL_15:
  a1[26] = v13;
  v9 = a1 + 27;
  if ( v16 == v9 )
  {
    if ( v5 != 0 )
    {
      v10 = v12 + 1;
      v9 = v11;
      goto LABEL_20;
    }
  }
  else if ( v5 != 0 )
  {
    (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: v11, a3: v12);
    v10 = 1;
    goto LABEL_20;
  }
LABEL_21:
  if ( *v6 == 0 )
    *v6 = 1;
  if ( v5 != 0 )
    (*(void (__fastcall **)(__int64, _BYTE *, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: v7, a3: 4);
  LOBYTE(v4) = *(_DWORD *)(v5 + 16) == 0;
  if ( _InterlockedDecrement((volatile signed __int32 *)(v5 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v5)(a1: v5, a2: 1);
  return (unsigned int)v4;
}
