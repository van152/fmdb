bool __fastcall sub_143EB4E80(__int64 a1, _QWORD *a2)
{
  __int64 v4; // r8
  __int64 v5; // r12
  __int64 v6; // r14
  __int64 v7; // r8
  bool v8; // zf
  __int64 v9; // r15
  __int64 v10; // rdi
  _QWORD *v11; // rdi

  v4 = a2[2];
  if ( a2[3] == a1 )
  {
    v5 = a1 + 7;
    v6 = a1 + 8;
    v8 = v4 == -7;
    v7 = v4 + 7;
    a2[2] = v7;
    a2[3] = a1 + 7;
    if ( v8 )
      goto LABEL_9;
  }
  else
  {
    if ( v4 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1]);
    a2[1] = a1;
    a2[2] = 7;
    v5 = a1 + 7;
    a2[3] = a1 + 7;
    v6 = a1 + 8;
    v7 = 7;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1], a3: v7);
LABEL_9:
  a2[1] = v6;
  a2[2] = 4;
  v9 = a1 + 12;
  a2[3] = a1 + 12;
  v10 = a1 + 14;
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6, a3: 4);
  a2[1] = v10;
  a2[2] = 1;
  a2[3] = a1 + 15;
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v10, a3: 1);
  a2[1] = v9;
  a2[2] = 2;
  a2[3] = v10;
  if ( (unsigned __int16)qword_141B60330 >= 0xDD0u )
  {
    if ( *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v9, a3: 2);
    a2[1] = v5;
    a2[2] = 1;
    a2[3] = v6;
  }
  v11 = a2 + 1;
  if ( a2[2] != 0 && *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v11);
  a2[3] = 0;
  a2[2] = 0;
  *v11 = 0;
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
