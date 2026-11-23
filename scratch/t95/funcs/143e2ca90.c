bool __fastcall sub_143E2CA90(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  _DWORD *v6; // rdi
  __int64 v7; // rdx
  bool result; // al

  v4 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(v4, a1 + 8, 4);
  result = false;
  if ( v4[4] == 0 )
  {
    v5 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
    if ( v5[4] == 0 )
    {
      v6 = (_DWORD *)*a2;
      v7 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
      (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v6 + 40LL))(v6, v7, 4);
      if ( v6[4] == 0 )
        return true;
    }
  }
  return result;
}
