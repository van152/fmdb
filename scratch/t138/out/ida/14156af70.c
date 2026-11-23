__int64 __fastcall sub_14156AF70(__int64 a1, _QWORD *a2)
{
  __int64 v4; // r8
  _QWORD *v5; // r12
  __int64 v6; // r8
  bool v7; // zf
  char *v8; // rbx
  __int64 v9; // r8
  __int64 result; // rax
  __int64 v11; // rcx
  char v12; // [rsp+2Dh] [rbp-3Bh] BYREF
  _BYTE v13[2]; // [rsp+2Eh] [rbp-3Ah] BYREF
  _BYTE v14[56]; // [rsp+30h] [rbp-38h] BYREF

  v4 = a2[2];
  if ( (_BYTE *)a2[3] == v13 )
  {
    v5 = a2 + 2;
    v7 = v4 == -2;
    v6 = v4 + 2;
    a2[2] = v6;
    a2[3] = v14;
    if ( v7 )
      goto LABEL_9;
  }
  else
  {
    if ( v4 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1]);
    a2[1] = v13;
    v5 = a2 + 2;
    a2[2] = 2;
    a2[3] = v14;
    v6 = 2;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1], a3: v6);
LABEL_9:
  a2[1] = a1;
  a2[2] = 4;
  a2[3] = a1 + 4;
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 4);
  a2[1] = a1 + 20;
  a2[2] = 10;
  a2[3] = a1 + 30;
  v8 = &v12;
  if ( (char *)(a1 + 30) == &v12 )
  {
    v9 = 11;
    v8 = (char *)(a1 + 20);
  }
  else
  {
    if ( *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 20, a3: 10);
    a2[2] = 0;
    a2[1] = &v12;
    v9 = 1;
  }
  a2[2] = v9;
  a2[3] = v13;
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, char *))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v8);
  a2[1] = a1 + 8;
  a2[2] = 9;
  result = a1 + 17;
  a2[3] = a1 + 17;
  if ( *a2 != 0 )
  {
    result = (*(__int64 (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 9);
    v11 = *a2;
    a2[1] = a1 + 4;
    a2[2] = 4;
    a2[3] = a1 + 8;
    if ( v11 != 0 )
      result = (*(__int64 (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v11 + 40LL))(
                 a1: v11,
                 a2: a1 + 4,
                 a3: 4);
  }
  else
  {
    *v5 = 4;
  }
  a2[1] = a1 + 30;
  a2[2] = 1;
  a2[3] = a1 + 31;
  return result;
}
