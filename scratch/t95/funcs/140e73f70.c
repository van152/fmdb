// THUNK ALIAS -> sub_143C4D560 (jmp:0x140e73f70->0x143c4d560)
char __fastcall sub_143C4D560(__int64 a1)
{
  __int64 *v1; // rdx
  char result; // al
  __int64 v3; // rcx
  __int16 v4; // [rsp+36h] [rbp-2h] BYREF

  v1 = *(__int64 **)(a1 + 24);
  result = 4;
  if ( v1 != *(__int64 **)(a1 + 32) )
  {
    v3 = *v1;
    if ( *v1 != 0 )
    {
      v4 = 0;
      return sub_1411BB2F0(v3, (unsigned int)&v4, (unsigned int)&v4, 0, 0);
    }
  }
  return result;
}
