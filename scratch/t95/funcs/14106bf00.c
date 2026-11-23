__int64 __fastcall sub_14106BF00(__int64 a1, _QWORD *a2)
{
  __int64 v3; // r9
  __int64 result; // rax
  __int64 (__fastcall ***v5)(_QWORD, __int64); // rcx
  _QWORD v6[3]; // [rsp+20h] [rbp-18h] BYREF

  sub_140FE3E30(v6, *a2);
  LOBYTE(v3) = 1;
  result = sub_14081D7C0(a1, 1, v6, v3);
  v5 = (__int64 (__fastcall ***)(_QWORD, __int64))v6[0];
  if ( v6[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v6[0] + 8LL)) == 0 )
    return (**v5)(v5, 1);
  return result;
}
