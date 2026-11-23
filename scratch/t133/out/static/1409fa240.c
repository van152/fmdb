bool __fastcall sub_1439299A0(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  _DWORD *v7; // rdi

  v4 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: a1 + 4, a3: 1);
  if ( v4[4] != 0 )
    return false;
  v5 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 2);
  if ( v5[4] != 0 )
    return false;
  v7 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: a1 + 2, a3: 2);
  return v7[4] == 0;
}
