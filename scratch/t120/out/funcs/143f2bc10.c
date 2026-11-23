bool __fastcall sub_143F2BC10(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rbx
  _DWORD *v7; // rdi
  __int64 v8; // rdx
  bool result; // al

  v4 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: a1 + 24, a3: 8);
  result = false;
  if ( v4[4] == 0 )
  {
    v5 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 4);
    if ( v5[4] == 0 )
    {
      v6 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 12, a3: 4);
      if ( *(_DWORD *)(v6 + 16) == 0 )
      {
        v7 = (_DWORD *)*a2;
        v8 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: v8, a3: 4);
        if ( v7[4] == 0 )
          return true;
      }
    }
  }
  return result;
}
