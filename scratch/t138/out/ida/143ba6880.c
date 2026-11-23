bool __fastcall sub_143BA6880(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rdi
  int v5; // esi
  _BYTE v7[17]; // [rsp+27h] [rbp-11h] BYREF

  v7[0] = 0;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v7, a3: 1);
  if ( (unsigned __int8)sub_14145CE40(a1, a2) == 0 )
    return false;
  v4 = *a2;
  if ( v4 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v4 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v4 + 40LL))(a1: v4, a2: a1 + 248, a3: 4);
  }
  v5 = *(_DWORD *)(v4 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v4 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v4)(a1: v4, a2: 1);
  return v5 == 0;
}
