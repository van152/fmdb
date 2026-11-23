bool __fastcall sub_1445FAE90(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  _DWORD *v9; // rdi
  int v10; // [rsp+28h] [rbp-20h] BYREF
  _BYTE v11[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  sub_140814B10(a1: *a2, a2: &v10, a3: a1);
  if ( v10 != 0 )
    return false;
  sub_140814B10(a1: *a2, a2: &v10, a3: a1 + 8);
  if ( v10 != 0 )
    return false;
  sub_140814B10(a1: *a2, a2: &v10, a3: a1 + 16);
  if ( v10 != 0 )
    return false;
  sub_140814B10(a1: *a2, a2: &v10, a3: a1 + 24);
  if ( v10 != 0 )
    return false;
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 32, a2) == 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 36, a3: 4);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 40, a3: 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 44, a3: 4);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v9 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2: a1 + 48, a3: 4);
  return v9[4] == 0;
}
