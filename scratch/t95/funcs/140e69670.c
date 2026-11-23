// THUNK ALIAS -> sub_143C3C8F0 (jmp:0x140e69670->0x143c3c8f0)
__int64 __fastcall sub_143C3C8F0(__int64 a1, char a2, __int64 a3)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  int v7; // r15d
  int v8; // r12d
  unsigned __int64 i; // rbp
  __int64 v10; // rdi
  __int64 v11; // rdx
  __int64 v12; // rax
  unsigned int v13; // eax
  __int64 v14; // rax
  __int64 v15; // rcx
  __int64 v16; // rbx
  unsigned int v17; // eax

  v4 = *(_QWORD *)(a1 + 24);
  v5 = *(_QWORD *)(a1 + 32);
  if ( v4 != v5 )
  {
    v7 = 16387;
    v8 = 1073995784;
    for ( i = 0; i < (v5 - v4) >> 3; ++i )
    {
      v10 = *(_QWORD *)(v4 + 8 * i);
      if ( v10 != 0 )
      {
        v11 = *(unsigned __int8 *)(v10 + 40);
        if ( (_BYTE)v11 != 0 )
        {
          if ( a2 == 0 )
            goto LABEL_17;
          v12 = *(_QWORD *)(v10 + 80);
          if ( v12 != 0 && *(_QWORD *)(v12 + 96) != 0 )
          {
            v13 = *(unsigned __int8 *)(v12 + 244);
            if ( v13 <= 0xE )
            {
              if ( _bittest(&v7, v13) )
                return v10;
            }
          }
          v14 = *(_QWORD *)(v10 + 48);
          v15 = 368;
          if ( *(_BYTE *)(v10 + 47) == 0 )
            v15 = 216;
          v16 = *(_QWORD *)(v14 + v15);
          if ( v16 == 0
            || (LOBYTE(a3) = 1, (unsigned __int8)sub_140CC6A10(*(_QWORD *)(v14 + v15), v11, a3, 0) == 0)
            || (unsigned __int8)sub_140CC6A10(v16, *(unsigned __int8 *)(v10 + 40), 0, 0) != 0 )
          {
LABEL_17:
            v17 = *(char *)(v10 + 40);
            if ( v17 <= 0x1E && _bittest(&v8, v17) )
              return v10;
          }
        }
        v4 = *(_QWORD *)(a1 + 24);
        v5 = *(_QWORD *)(a1 + 32);
      }
    }
  }
  return 0;
}
