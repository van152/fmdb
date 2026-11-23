// THUNK ALIAS -> sub_143C30820 (jmp:0x140e64e50->0x143c30820)
__int64 __fastcall sub_143C30820(_QWORD *a1)
{
  __int64 result; // rax
  __int64 *v2; // rax
  __int64 v3; // r8
  __int64 v4; // rdx
  __int64 v5; // rdx
  __int64 *v6; // rcx
  __int64 v7; // rcx
  bool v8; // zf

  result = a1[31];
  if ( result == 0 )
  {
    if ( (_BYTE)word_141B60320 == 0 )
      return 0;
    v2 = (__int64 *)a1[3];
    if ( v2 == (__int64 *)a1[4] )
    {
      return 0;
    }
    else
    {
      v3 = *v2;
      result = 0;
      while ( 1 )
      {
        v4 = *(_QWORD *)(v3 + 120);
        if ( v4 != 0 )
          break;
        v5 = *(_QWORD *)(v3 + 48);
        if ( v5 != 0 )
        {
          v6 = *(__int64 **)(v5 + 24);
          if ( *(__int64 **)(v5 + 32) != v6 )
          {
            v7 = *v6;
            v8 = v7 == v3;
            v3 = v7;
            if ( !v8 )
              continue;
          }
        }
        return result;
      }
      return *(_QWORD *)(v4 + 80);
    }
  }
  return result;
}
