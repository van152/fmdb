bool __fastcall sub_14442DFB0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  _DWORD *v9; // rdi

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, 0x1418B8FF0LL, 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140F944F0(&qword_141B5FDA8, *(_QWORD *)(a1 + 8), a2, (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 16, 2);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 18, 2);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 20, 1);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v9 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v9 + 40LL))(v9, a1 + 21, 1);
  return v9[4] == 0;
}
