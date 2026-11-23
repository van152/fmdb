bool __fastcall sub_143B48DB0(__int64 a1, __int64 *a2)
{
  __int64 v2; // rsi
  int v3; // edi

  v2 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v2 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v2 + 40LL))(a1: v2, a2: a1, a3: 4);
  }
  v3 = *(_DWORD *)(v2 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v2 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v2)(a1: v2, a2: 1);
  return v3 == 0;
}
