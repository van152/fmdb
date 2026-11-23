// THUNK ALIAS -> sub_143C31720 (jmp:0x140e65660->0x143c31720)
char __fastcall sub_143C31720(__int64 a1)
{
  __int64 *v2; // rax
  __int64 v3; // rcx
  char result; // al
  __int64 v5; // r14
  __int64 *v6; // rax
  __int64 *v7; // rdx
  int v8; // r8d
  __int64 v9; // rsi
  unsigned int v10; // ebx
  unsigned __int16 v11; // cx
  __int64 v12; // rcx
  char v13; // cl

  if ( *(_QWORD *)(a1 + 216) == 0 )
    return 0;
  v2 = *(__int64 **)(a1 + 24);
  if ( v2 == *(__int64 **)(a1 + 32) )
    return 0;
  v3 = *v2;
  if ( *v2 == 0 )
    return 0;
  result = 0;
  if ( *(_QWORD *)(v3 + 48) != 0 )
  {
    v5 = *(_QWORD *)(v3 + 80);
    if ( v5 != 0 )
    {
      v6 = *(__int64 **)(a1 + 280);
      v7 = *(__int64 **)(a1 + 288);
      if ( v6 != v7 )
      {
        v8 = 1049072;
        while ( 1 )
        {
          v9 = *v6;
          if ( *(_QWORD *)(*v6 + 8) == a1 )
          {
            v10 = *(unsigned __int8 *)(v9 + 48);
            if ( v10 <= 0x14 )
            {
              if ( _bittest(&v8, v10) )
                break;
            }
          }
          if ( ++v6 == v7 )
            goto LABEL_13;
        }
        if ( *(_QWORD *)v9 != 0 )
          return 0;
      }
LABEL_13:
      if ( (unsigned __int8)sub_1411BB660() != 0 || (*(_BYTE *)(a1 + 353) & 0x40) != 0 )
        return 0;
      if ( *(_DWORD *)(a1 + 12) == 1573 )
      {
        v11 = word_141AB0260;
        if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
        {
          word_141AB0260 = 2023;
          v11 = 2023;
        }
        if ( HIWORD(dword_141AAE084) <= v11 && (char)sub_140DB9C10(&dword_141AAE084) < 10 )
          return 0;
      }
      v12 = *(_QWORD *)(v5 + 176);
      if ( v12 == 0 )
        return 0;
      if ( !sub_1409083C0(v12) )
        return 0;
      v13 = sub_140ECF770(v5);
      result = 1;
      if ( v13 != 0 )
        return 0;
    }
  }
  return result;
}
