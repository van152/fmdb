bool __fastcall sub_143B48E40(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  _DWORD *v6; // rdi

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1, 2);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v6 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v6 + 40LL))(v6, a1 + 2, 2);
  return v6[4] == 0;
}
