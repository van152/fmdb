// THUNK ALIAS -> sub_143C4C980 (jmp:0x140e71eb0->0x143c4c980)
__int64 __fastcall sub_143C4C980(__int64 a1)
{
  __int64 **v1; // rax
  __int64 *v2; // rdx
  __int64 *v3; // r8
  __int64 result; // rax
  int v5; // r9d
  unsigned __int16 v6; // r10
  __int64 v7; // r11

  v1 = *(__int64 ***)(qword_141B601D0 + 128);
  v2 = *v1;
  v3 = v1[1];
  result = 0;
  if ( v2 != v3 )
  {
    v5 = *(_DWORD *)(a1 + 12);
    v6 = word_141AB0260;
    while ( 1 )
    {
      v7 = *v2;
      if ( *(_DWORD *)(*v2 + 24) == v5 )
      {
        if ( v6 >= 0x7E8u )
        {
          word_141AB0260 = 2023;
          v6 = 2023;
        }
        if ( *(_WORD *)(v7 + 32) == v6 )
          break;
      }
      if ( ++v2 == v3 )
        return result;
    }
    return *(unsigned int *)(v7 + 28);
  }
  return result;
}
