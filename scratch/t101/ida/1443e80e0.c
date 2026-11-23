bool __fastcall sub_1443E80E0(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, 0x1418B89A8LL, 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140F80810(*a1, a2, (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 18, 1);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 19, 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 20, 1);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140F80640(a1[1], a2, 3 * (unsigned int)(byte_141B5FC2C == 0)) == 0 )
    return false;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 21, 1);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 2, 2);
  return *(_DWORD *)(v9 + 16) == 0 && *(_DWORD *)(*a2 + 16LL) == 0;
}
