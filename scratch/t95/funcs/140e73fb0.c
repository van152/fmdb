// THUNK ALIAS -> sub_143C4D600 (jmp:0x140e73fb0->0x143c4d600)
__int64 __fastcall sub_143C4D600(__int64 a1)
{
  __int64 *v1; // rax
  __int64 v2; // rcx
  unsigned __int16 v4; // [rsp+34h] [rbp-4h] BYREF
  __int16 v5; // [rsp+36h] [rbp-2h] BYREF

  v1 = *(__int64 **)(a1 + 24);
  if ( v1 == *(__int64 **)(a1 + 32) )
    return 0;
  v2 = *v1;
  if ( *v1 == 0 )
    return 0;
  v5 = 0;
  v4 = 0;
  sub_1411BB2F0(v2, (unsigned int)&v4, (unsigned int)&v5, 0, 0);
  return v4;
}
