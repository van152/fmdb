__int64 __fastcall sub_1442A9820(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx

  v4 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: a1 + 18, a3: 1);
  if ( v4[4] != 0 )
    return 0;
  v5 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 19, a3: 1);
  if ( v5[4] != 0 )
    return 0;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 20, a3: 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return 0;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 16, a3: 2);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return 0;
  else
    return sub_1413C4780(a1, a2);
}
