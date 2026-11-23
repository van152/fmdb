// THUNK ALIAS -> sub_14401BBA0 (jmp:0x1411e1ce0->0x14401bba0)
__int64 __fastcall sub_14401BBA0(__int64 a1, __int64 a2)
{
  __int64 v3; // rax
  unsigned int v4; // edx
  bool v5; // zf
  __int64 result; // rax

  v3 = sub_141751B70(*(_QWORD *)(a1 + 24), *(_QWORD *)(a1 + 32), a2);
  v4 = (unsigned int)(v3 - *(_DWORD *)(a1 + 24)) >> 3;
  v5 = v3 == *(_QWORD *)(a1 + 32);
  result = 255;
  if ( !v5 )
    return v4;
  return result;
}
