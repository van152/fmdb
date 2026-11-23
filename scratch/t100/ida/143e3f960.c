bool __fastcall sub_143E3F960(_DWORD *a1, __int64 *a2)
{
  __int64 v3; // rsi
  int v4; // edi

  v3 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v3 + 8));
    (*(void (__fastcall **)(__int64, _DWORD *, __int64))(*(_QWORD *)v3 + 40LL))(v3, a1, 8);
  }
  if ( a1[1] == 0 )
    a1[1] = *a1;
  v4 = *(_DWORD *)(v3 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v3 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v3)(v3, 1);
  return v4 == 0;
}
