char __fastcall sub_1442E1FF0(__int64 a1, int a2, int a3)
{
  __int64 v4; // rcx
  char v5; // bl
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  char v7; // si
  char result; // al
  __int64 v9; // [rsp+40h] [rbp-28h] BYREF
  __int64 v10; // [rsp+48h] [rbp-20h] BYREF
  __int64 v11; // [rsp+50h] [rbp-18h] BYREF

  v11 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v11,
    a2: (unsigned int)&v10,
    a3: a2,
    a4: a3,
    a5: (__int64)&unk_141B662A0,
    a6: 0,
    a7: 0,
    0);
  v4 = v10;
  if ( v10 == 0 )
    return 0;
  if ( SBYTE4(v11) < 30 )
    goto LABEL_11;
  v9 = v10;
  _InterlockedIncrement((volatile signed __int32 *)(v10 + 8));
  v5 = sub_1413EE550(a1, a2: &v9);
  v6 = (void (__fastcall ***)(_QWORD, __int64))v9;
  if ( v9 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v9 + 8)) == 0 )
    (**v6)(a1: v6, a2: 1);
  v4 = v10;
  if ( v5 == 0 )
  {
    if ( v10 != 0 )
    {
LABEL_11:
      v7 = 0;
      result = 0;
      if ( _InterlockedDecrement((volatile signed __int32 *)(v4 + 8)) != 0 )
        return result;
LABEL_12:
      (**(void (__fastcall ***)(__int64, __int64))v4)(a1: v4, a2: 1);
      return v7;
    }
    return 0;
  }
  if ( v10 == 0 )
    return 1;
  v7 = 1;
  result = 1;
  if ( _InterlockedDecrement((volatile signed __int32 *)(v10 + 8)) == 0 )
    goto LABEL_12;
  return result;
}
