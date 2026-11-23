// THUNK ALIAS -> sub_144016150 (jmp:0x1411dc9e0->0x144016150)
__int64 __fastcall sub_144016150(_QWORD *a1)
{
  char v2; // cl
  __int64 result; // rax
  __int64 v4; // rcx
  __int64 i; // r9
  __int64 v6; // rdx

  v2 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60);
  result = (__int64)(a1[4] - a1[3]) >> 3;
  if ( v2 != 0 )
  {
    v4 = a1[6];
    for ( i = a1[7]; v4 != i; v4 += 8 )
    {
      v6 = 368;
      if ( *(_BYTE *)(*(_QWORD *)v4 + 47LL) == 0 )
        v6 = 216;
      result -= (*(_QWORD *)(*(_QWORD *)(*(_QWORD *)v4 + 48LL) + v6) == 0) - 1LL;
    }
  }
  else
  {
    result += (__int64)(a1[7] - a1[6]) >> 3;
  }
  return result;
}
